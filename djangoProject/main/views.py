import logging

from django.http import HttpRequest
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from .result import R
from .utils import JiebaUtils, CommonUtils

# 实例化 JiebaUtils 对象
jieba_utils = JiebaUtils()
cache_dict: dict = dict()
logger = logging.getLogger(__name__)


# 测试
@csrf_exempt
def example(request: HttpRequest):
    utils_get_data = CommonUtils.getRequestParams(request=request)
    utils_get_data.update({'csrf_token': get_token(request)})
    result_vo = R(data=utils_get_data)
    # 设置 safe=False 允许序列化非字典对象
    return JsonResponse(result_vo.to_dict())


# 分词搜索产品
@csrf_exempt
def search_1(request: HttpRequest):
    utils_get_data = CommonUtils.getRequestParams(request)
    keyword = utils_get_data.get("keyword")
    products = jieba_utils.search_product_1(input_text=keyword)
    return JsonResponse(R(data=products).to_dict())


# 分词搜索产品
@csrf_exempt
def search(request: HttpRequest):
    utils_get_data = CommonUtils.getRequestParams(request)
    keyword = utils_get_data.get("keyword")
    logger.info("Searching keyword=" + keyword)
    if cache_dict.get(keyword) is None:
        products = jieba_utils.search_product(keyword)
        if len(keyword) < 250:
            cache_dict.update({keyword: products})
        return JsonResponse(R(data=products).to_dict())
    else:
        return JsonResponse(R(data=cache_dict.get(keyword)).to_dict())


# 分词搜索产品
@csrf_exempt
def search_2(request: HttpRequest):
    utils_get_data = CommonUtils.getRequestParams(request)
    keyword = utils_get_data.get("keyword")
    products = jieba_utils.search_product_2(keyword)
    return JsonResponse(R(data=products).to_dict())
