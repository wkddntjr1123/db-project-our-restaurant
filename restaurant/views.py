from django.core.paginator import EmptyPage, Paginator
from django.db.models.expressions import F
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, Restaurant
from django.db.models import Q
from django.forms.models import model_to_dict
from authentication.models import Group, GroupAndMember, User
import os, json


def index(request):
    return render(request, "restaurant/index.html")


def bulkInsert(request):
    with open(f"{os.path.abspath(os.path.dirname(__file__))}\data.json", encoding="utf8") as datas:
        items = json.loads(datas.read())
        for item in items:
            Restaurant.objects.create(
                name=item.get("name", ""),
                menus=item.get("menus", ""),
                phone=item.get("phone", ""),
                roadAddr=item.get("roadNameAddress", ""),
                numberAddr=item.get("numberAddress", ""),
                latitude=item.get("latitude", ""),
                longitude=item.get("longitude", ""),
            )
    return JsonResponse({"a": "b"})


# 맵 idle 이벤트에 따라서 지도 영역(좌하단~우상단 위도 경도)의 포스트들을 Json return
# 추가적으로 filtering관련된 파라미터를 받으면 필터링 된 포스트들을 Json return
def getBoundaryPost(request):
    swLat = request.GET.get("swLat")
    swLng = request.GET.get("swLng")
    neLat = request.GET.get("neLat")
    neLng = request.GET.get("neLng")

    # 필터링이 적용된 경우
    boundPosts_querySet = []
    if request.GET.get("isFiltering"):
        filters = {}
        if request.GET.get("name"):
            filters["name__icontains"] = request.GET.get("name")
        if request.GET.get("menus"):
            filters["menus__icontains"] = request.GET.get("menus")

        boundPosts_querySet = Restaurant.objects.filter(
            **filters, latitude__range=(swLat, neLat), longitude__range=(swLng, neLng)
        )
        if request.GET.get("location"):
            boundPosts_querySet = boundPosts_querySet.filter(
                Q(roadAddr__icontains=request.GET.get("location"))
                | Q(numberAddr__icontains=request.GET.get("location"))
            )
    elif request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
        boundPosts_querySet = Restaurant.objects.filter(
            Q(name__icontains=keyword)
            | Q(menus__icontains=keyword)
            | Q(roadAddr__icontains=keyword)
            | Q(numberAddr__icontains=keyword)
            | Q(phone__icontains=keyword),
            latitude__range=(swLat, neLat),
            longitude__range=(swLng, neLng),
        )
    else:
        # select : id,제목,위도,경도,분류id, db한번만 접근하도록 미리 FK역참조 정보 classification 같이 가져옴
        boundPosts_querySet = Restaurant.objects.filter(
            latitude__range=(swLat, neLat),
            longitude__range=(swLng, neLng),
        )
    rawBoundPosts = list(
        boundPosts_querySet.values(
            "id",
            "name",
            "menus",
            "phone",
            "roadAddr",
            "numberAddr",
            "latitude",
            "longitude",
        )
    )

    boundPosts = json.dumps(list(rawBoundPosts), default=str)

    return JsonResponse(boundPosts, safe=False)


# page번호를 받아서 해당 page에 해당하는 post10개와 페이지네이션 범위를 json리턴
def getPagedPost(request, page):
    posts = []
    if request.GET.get("isFiltering"):
        filters = {}
        if request.GET.get("name"):
            filters["name__icontains"] = request.GET.get("name")
        if request.GET.get("menus"):
            filters["menus__icontains"] = request.GET.get("menus")
        posts = Restaurant.objects.filter(**filters)
        if request.GET.get("location"):
            posts = posts.filter(
                Q(roadAddr__icontains=request.GET.get("location"))
                | Q(numberAddr__icontains=request.GET.get("location"))
            )
    elif request.GET.get("keyword"):
        keyword = request.GET.get("keyword")
        posts = Restaurant.objects.filter(
            Q(name__icontains=keyword)
            | Q(menus__icontains=keyword)
            | Q(roadAddr__icontains=keyword)
            | Q(numberAddr__icontains=keyword)
            | Q(phone__icontains=keyword)
        )
    else:
        posts = Restaurant.objects.all().order_by("-id")  # DB에서 post자료 모두 받아오기

    # 첫번째인자로 페이지로 분할될 객체, 두번째인자로 한 페이지에 담길 객체 수
    paginator = Paginator(posts, 15)
    try:
        page_obj = paginator.get_page(page)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # page range
    page_range = []
    for i in paginator.page_range:
        page_range.append(i)

    # paged_posts
    paged_posts = []
    for post in page_obj:
        item = model_to_dict(
            post,
            fields=[
                "id",
                "name",
                "phone",
                "menus",
                "roadAddr",
                "numberAddr",
                "latitude",
                "longitude",
            ],
        )
        paged_posts.append(item)
    pageFirst = page_range[0]
    pageLast = page_range[-1]

    pagePrev = None
    pageNext = None
    if page <= 4:
        pagePrev = 1
    else:
        pagePrev = page - 3

    if page >= pageLast - 3:
        pageNext = pageLast
        pagePrev = page - 3
    else:
        pageNext = page + 3

    if pagePrev > pageNext:
        pagePrev = pageNext
    if pagePrev < 1:
        pagePrev = 1
    return JsonResponse(
        {
            "pageFirst": pageFirst,
            "pagePrev": pagePrev,
            "pageNext": pageNext,
            "pageLast": pageLast,
            "posts": paged_posts,
            "currentPage": page,
        }
    )


def getOverlayInfo(request, post_id):
    post = Restaurant.objects.get(pk=post_id)
    return JsonResponse(
        {
            "name": post.name,
            "menus": post.menus,
            "phone": post.phone,
            "roadAddr": post.roadAddr,
            "numberAddr": post.numberAddr,
        }
    )


# post하나의 정보를 Json return
def getPostData(request, id):
    rawPost = Restaurant.objects.get(pk=id)
    comments = rawPost.comment_set.all().values()
    commentsData = []
    if len(comments):
        for comment in comments:
            user = model_to_dict(
                User.objects.get(id=comment["writer_id"]), ["name", "nickname", "id"]
            )
            score = comment["score"]
            contents = comment["contents"]
            commentsData.append(
                {"id": comment["id"], "user": user, "score": score, "contents": contents}
            )
        returnObject = model_to_dict(rawPost)
        returnObject.update({"comments": commentsData})
    else:
        returnObject = model_to_dict(rawPost)
    return JsonResponse(returnObject, safe=False)


# comment등록
@csrf_exempt
def createComment(request):
    restaurant = Restaurant.objects.get(id=request.POST["id"])
    writer = request.user
    contents = request.POST["contents"]
    score = request.POST["score"]
    commentObj = Comment.objects.create(
        restaurant=restaurant, writer=writer, contents=contents, score=score
    )
    return JsonResponse(model_to_dict(commentObj), safe=False)


# comment삭제
@csrf_exempt
def deleteComment(request):
    id = request.POST["id"]
    comment = Comment.objects.get(id=id)
    postId = comment.restaurant.id
    comment.delete()
    return JsonResponse({"postId": postId})


def getGroupReviewData(request, id):
    user = request.user
    rawComments = Comment.objects.filter(restaurant_id=id)
    groupComments = []
    groupIdDomain = []
    rawGroupDomain = GroupAndMember.objects.filter(user=request.user).values_list("group_id")
    for group in rawGroupDomain:
        groupIdDomain.append(group[0])

    for comment in rawComments:
        dictComment = model_to_dict(comment)
        rawGroups = GroupAndMember.objects.filter(user=comment.writer).values_list("group_id")
        commentGroupDomain = []
        for group in rawGroups:
            commentGroupDomain.append(group[0])

        intersectGroupId = set(groupIdDomain) & set(commentGroupDomain)
        if len(intersectGroupId):
            groupComments.append(
                {
                    "id": dictComment["id"],
                    "user": model_to_dict(user, ["id", "nickname"]),
                    "score": dictComment["score"],
                    "contents": dictComment["contents"],
                }
            )
    return JsonResponse(groupComments, safe=False)
