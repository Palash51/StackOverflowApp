import re

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
from django.conf import settings
from Stackexchange.response import api_response
from helpers import get_timestamp, get_logged_user
from scripts.chrome_history import update_user_history
from searchapp.models import User, MarkedUrl
from searchapp.serializers import SignupSerializer, StackOverflowQuestionSerializer, MarkedUrlSerializer
from searchapp.stackexchange import get_stack_overflow_client
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

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
    cache.set("SE_token", token.key, timeout=CACHE_TTL)
    print(cache.keys('*'))

    update_user_history(user)

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

@csrf_exempt
@api_view(["GET", "POST"])
@throttle_classes([])
@permission_classes((IsAuthenticated,))
@api_response
def signout(request):
    """user's session will be deleted"""
    user = request.user
    user.auth_token.delete()
    request.session.delete()
    cache.delete('SE_token')
    return {'status': 1, "data": "You have successfully logged out"}



class SearchView(APIView):
    """
    search user queries -
    1) madatory field - question (query)
    2) optional filters - sort questions, date filter
    3) page size -10
    4) request will be cached for 10 min
    """

    permission_classes = (IsAuthenticated,)

    # @method_decorator(cache_page(60 * 10))
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



class MarkedLink(APIView):
    """
    user will mark the link as known
    """
    permission_classes = (AllowAny,)


    @api_response
    def get(self, request):
        """get the list of all the marked links"""

        user = get_logged_user()
        all_urls = MarkedUrl.objects.filter(user=user).order_by('created_at')
        serializer_context = {
            'request': request,
        }
        data = MarkedUrlSerializer(all_urls, context=serializer_context, many=True).data

        return {"status": 1, "data": data}


    @api_response
    def post(self, request):
        """
        :param request:
        :return: users marked url
        """
        url = request.data['url']
        user = get_logged_user()
        try:
            question_id = [i for i in re.findall('\d+', url) if len(i) > 4][0]
            if question_id:
                stack_overflow = get_stack_overflow_client()
                question = stack_overflow.questions(question_id)
                question_title = question.items[0].title
                new_mark = MarkedUrl.objects.get_or_create(
                    user=user,
                    url=request.data['url'],
                    marked=request.data['marked'],
                    title=question_title
                )
                return {"status": 1, "data": "created"}
            return {"status": 0, "data": "Marked Url is not a stackoverflow url"}

        except Exception:
            return {"status": 0, "data": "Marked Url is not a stackoverflow url"}


