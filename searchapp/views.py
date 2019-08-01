from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from Stackexchange.response import api_response
from helpers import get_timestamp
from searchapp.models import User
from searchapp.serializers import SignupSerializer, StackOverflowQuestionSerializer
from searchapp.stackexchange import get_stack_overflow_client


class Signup(APIView):
    """
    user signup api
    """
    permission_classes = (AllowAny,)
    throttle_classes =  ([])

    @api_response
    def post(self, request, format='json', **kwargs):

        data = dict(request.data)
        ser_user = SignupSerializer(data=data)

        if not ser_user.is_valid():
            return {'status': 0, 'message': ser_user.sg_errors}
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            mobile_number=data['mobile_number'],
        )
        user.set_password(data['password'])

        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        res = {}
        res.update({
            'uid': user.id,
            'username': user.email,
            'token': token.key,
            'first_name': user.first_name or "",
            'last_name': user.last_name or "",
            'email': user.email,
        })
        return {'status': 1, 'data': res}


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@throttle_classes([])
@api_response
def signin(request):
    """
    :param request:
    :return: return user token everytime user logged in
    """
    data = request.data
    username = data.get("username");
    password = request.data.get("password")
    if not username or not password:
        return {'status': 0, 'message': "Please provide both username and password"}


    user = authenticate(username=username, password=password)
    if not user:
        return {'status': 0, 'message': "Invalid credentials!", 'statusCode': 401}

    try:
        if user.auth_token:
            user.auth_token.delete()
    except Exception:
        pass


    user.last_login = timezone.now()
    user.save()

    token, _ = Token.objects.get_or_create(user=user)
    user_data = {
        'token': token.key,
        'user': user.username,
        'uid': token.user_id,
        'first_name': user.first_name or "",
        'last_name': user.last_name or "",
        'email': user.email or ""
    }
    return {
        'status': 1,
        'data': user_data
    }



class SearchView(APIView):
    """
    search user queries -
    1) madatory field - question (query)
    2) optional filters - sort questions, date filter
    3) page size -10
    4) request will be cached for 10 min
    """

    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(60 * 10))
    @api_response
    def get(self, request):
        try:
            pnp = PageNumberPagination()
            pnp.page_size = 10

            stack_overflow = get_stack_overflow_client()
            filter_kwargs = {'intitle':request.query_params.get('search_query'), 'pagesize':100}
            sort_filter = request.query_params.get('sort')
            date_filter_fromdate = request.query_params.get('fromdate')
            date_filter_todate = request.query_params.get('todate')

            if sort_filter:
                filter_kwargs.update({'sort':sort_filter})

            if date_filter_fromdate and date_filter_todate:
                fromdate = get_timestamp(date_filter_fromdate)
                todate = get_timestamp(date_filter_todate)
                filter_kwargs.update({
                    'fromdate':fromdate,
                    'todate': todate
                })

            queries = stack_overflow.search(**filter_kwargs).items
            page = pnp.paginate_queryset(queries, request)

            data = {
                'count': pnp.page.paginator.count,
                'previous': pnp.get_previous_link(),
                'next': pnp.get_next_link(),
                'total_pages': pnp.page.paginator.num_pages,
                'results': StackOverflowQuestionSerializer(page, many=True).data,
            }

            return {"status": 1, "data": data}

        except Exception as e:
            return {"status": 0, "data": "Unable to fetch data"}




@csrf_exempt
@api_view(["GET", "POST"])
@throttle_classes([])
@permission_classes((IsAuthenticated,))
@api_response
def signout(request):
    """user's session will be deleted"""
    user = request.user
    user.auth_token.delete()
    return {'status': 1, "data": "You have successfully logged out"}





