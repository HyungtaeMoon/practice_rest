from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


# @api_view(['GET', 'POST'])
# def product_list(request, format=None):
#     """
#     Product 또는 새로운 Product 생성
#     """
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    """상품을 모두 보여주거나 새로운 상품을 생성"""
    # serializer_class 에 직렬화 모델을 정의하여 Content 안에 시리얼라이저 모델의 필드에 접근
    # 만약 정의하지 않는다면 POST 로 접근해도 필드값이 없이 Content 만 나옴
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCopyInstance(APIView):
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoestNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        response = self.get_object(pk=pk)
        serializer = ProductSerializer(response)
        return Response(serializer.data)

    def post(self, request, pk, format=None, **kwargs):
        """
        복사하여 새로운 객체를 만들어주기 때문에 POST 메서드로 사용하기 도전
        그럼 instance=request.data 와 같이 어떤 객체인지를 먼저 알게 해줘야 할 듯

        ### ORM CookBook 을 참고하여 아이디어를 얻음 ###
        Product.objects.all().count() # 4

        coffee = Product.objects.first()

        coffee.pk = None

        coffee.save()

        Product.objects.all().count() # 5
        """
        # 현재 해당하는 객체의 pk 가 무엇인지까지 확인
        # kwargs 는 해당하는 딕셔너리에서 key 값만을 불러옴
        # POST 메서드에서 data 를 불러오면 새로 입력한 값들이 들어오기 때문에 .data 는 피해야 함
        # original_data = self.kwargs.get('pk', '')
        # 생성하려는 객체를 만들기 위해 우선 Product 모델에서 불러오기(아직 직렬화 상태 아님)
        product = Product.objects.get(pk=pk)
        product.pk = None
        # 직렬화 상태(serializer) 로 만듦
        # 이 클래스에서 get 메서드를 통해 들어온 request.data 를 data 로 받아 직렬화
        # 매직메서드 __dict__ 의 사용방법은 느낌적으로 옳지 않은 것 같지만 일단은 구현을 위해 사용
        serializer = ProductSerializer(product, data=product.__dict__)
        additional_data = serializer
        if additional_data.is_valid():
            # save() 함수를 사용하기 위해서는 is_valid() 가 필수(아니면 에러 발생)
            additional_data.save()
            return Response(additional_data.data, status=status.HTTP_201_CREATED)
        return Response(additional_data.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk, format=None):
#     """
#     product 조회, 업데이트, 삭제
#     """
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(APIView):
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
