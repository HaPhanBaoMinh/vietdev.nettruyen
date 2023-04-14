# `Hướng dẫn Todolist backend`

## Giới thiệu

tôi đang làm quen với lập trình web back-end sử dụng django, tôi đã sử dụng công nghệ này để tạo ra một trang web đơn giản là list ra các công việc cần làm hằng ngày.

## Tạo project

Để bắt đầu với một project back-end bằng django, bước đầu tiên đó là tạo môi trường cho project. Sau khi cài python, django và setup môi trường, tôi sẽ bắt đầu dự án đầu tiên có tên ToDoList bằng cách gõ lệnh sau vào cmd:

```console
django startproject ToDoList
```

Sau khi khởi tạo project, chúng ta sẽ có được cây thư mục như sau:

```
ToDoList
|_____ToDoList
|  |_____ __init__.py
|  |_____asgi.py
|  |_____setting.py
|  |_____url.py
|  |_____wsgi.py
|_____manage.py
```

Ở trên là những bước tạo một webserver, bây giờ tôi sẽ tạo một ứng dụng web có tên là Home trên server này.

```console
python manage.py startapp Home
```

Một thư mục với tên Home sẽ được tạo ra và có cấu trúc như sau:

```
Home
|_____migrations
|  |_______init__.py
|_______init__.py
|_____admin.py
|_____app.py
|_____models.py
|_____tests.py
|_____views.py
```

Một project bao gồm nhiều app và mỗi app thực hiện một công việc riêng biệt.
Để django nhận diện dứng dụng mới cài đặt và sử dụng nó, ta phải thêm <app_name> vào tệp setting.py vào mục INSTALLED_APP

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Home',
]
```

Chúng ta có thể cài đặt cấu hình của DataBase bằng mục DATABASES trong file setting.py. Ở đây, tôi sử dụng SQLite như mặc định của django nên không sửa.

Tôi sẽ setup môi trường bằng lệnh:

```console
python -m venv venv
```

# Models và Databases

Models là phần định nghĩa mô hình dữ liệu của Django. Ở project của tôi sẽ có 2 models chính có quan hệ one-to-many với nhau.

```python
from django.db import models

# Create your models here.
class List(models.Model):
    list_create_at = models.DateTimeField(auto_now_add=True)
    list_update_at = models.DateTimeField(auto_now=True)
    ping = models.BooleanField(default=False)
    list_completed = models.BooleanField(default=False)
    list_removed = models.BooleanField(default=False)


class ListDo(models.Model):
    order = models.IntegerField(default=0)
    color_bg = models.CharField(default="fff", blank=True, max_length=100)
    content = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    removed = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)
```

Ở models thứ nhất là models List, models này khai báo tất cả những list công việc gồm những trường như:

- Trường `list_create_at` và `trường list_update_at` dùng để ghi thời gian tạo và thời gian chỉnh sửa list, được set giá trị auto.
- Trường `ping` để ghim list lên đầu.
- Trường `list_completed` để đánh dấu là list công việc này được hoàn thành hay chưa.
- Trường `list_removed` để đánh dấu là list này đã bị xóa chưa, thay vì xóa luôn cả list thì chỉ cần đổi giá trị của biến `list_removed` về giá trị True, sau đó không hiển thị nữa nhưng vẫn còn lưu ở database.

Ở models `ListDo` là những công việc có trong một `list` được khai báo ở trên. Những trường trong `ListDo` gồm có:

- `order`: là một trường để lưu thứ tự của các công việc với giá trị mặc định bằng 0.
- `color_bg`: là một trường để lưu màu background.
- `content`: là trường lưu nội dung của công việc cần làm.
- `is_completed`: là trường Boolean dùng để đánh dấu là công việc đã hoàn thành hay chưa, giá trị mặc định của trường này là False.
- `create_at` và `update_at`: là hai trường dùng để lưu trữ thời gian tạo và thời gian thay đổi của models.
- `removed`: là trường để đánh dấu công việc đó bị xóa hay chưa, thay vị delete luôn dữ liệu của models thì chúng ta chỉ cần đổi giá trị này thành true và không xuất hiện trên font end nữa.
- `list`: là trường dùng để tham chiếu đến models `List`

Quan hệ giữa 2 model ở đây là quan hệ một-nhiều, một `List` nhiều `ListDo`.

Sau khi viết xong models, chúng ta sẽ tạo một file `serilizer.py` và viết các serilizer cho các models. Serialization là một quá trình để chuyển đổi một cấu trúc dữ liệu hoặc đối tượng thành một định dạng có thể lưu trữ được (ví dụ như trong một file, bộ nhớ, hoặc vận chuyển thông qua mạng).

```python
from rest_framework import serializers
from .models import ListDo, List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = (
            'id',
            'list_create_at',
            'list_update_at',
            'list_removed',
            'ping',
            'list_completed',
        )

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListDo
        fields = (
            'id',
            'order',
            'color_bg',
            'content',
            'is_completed',
            'created_at',
            'updated_at',
            'removed',
            'list',
        )
```

# Tạo Views

Chúng ta sẽ sử dụng file `views.py` để viết các api.

```python
from rest_framework.response import Response
from rest_framework import status, generics,viewsets
from rest_framework.views import APIView
from rest_framework import serializers
from .models import ListDo, List
from .serializers import ToDoListSerializer, ListSerializer
```

Đầu tiên chúng ta cần import những thư viện cần thiết, ví dụ như các models đã viết ở file `models.py`, `serilizer.py` và rest_framework để viết các API một cách dễ dàng hơn.

Tạo lớp ToDoListApiView để viết các hàm get, post, delete mà không cần giá trị id đầu vào.

```python
class ToDoListApiView(generics.ListCreateAPIView):
    #ListCreateAPIView cung cấp phương thức xử lý get và post, hỗ trợ insert data dễ hơn APIView
    queryset = ListDo.objects.filter(removed=False)
    serializer_class = ToDoListSerializer
    #phương thức get không có id dùng để get tất cả các data trong ListDo, kể cả trường list, nhưng trường list ở đây chỉ trả về giá trị là id của list mà ListDo tham chiếu tới
    def get(self, request):
        #lúc get dữ liệu chỉ lấy những object có trường removed=False
        obj = ListDo.objects.filter(removed=False)
        serializer = ToDoListSerializer(obj, many=True)
        return Response(serializer.data, status=200)

    #Phương thức post chỉ được chọn object list chứ không nhập một list mới được
    def post(self, request):

        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    #update trường removed=True cho tất cả các object có trong ListDo
    def delete(self, request):
        todo = ListDo.objects.all()
        for obj in todo:
            obj.removed = True
            serializer = ToDoListSerializer(data=obj)
            if serializer.is_valid():
                serializer.save()
            obj.save()
        return Response({'msg': 'all deleted'}, status=status.HTTP_204_NO_CONTENT)
```

Để gọi thực thi các hàm trong lớp ToDoListApiView, chúng ta phải tham chiếu tới hàm ToDoListApiView trong file urls.py.

Ở thư mục ToDoList tạo ra bởi lệnh `startproject`, có một tệp urls.py, tại đây sẽ khai báo các đường dẫn mà website dẫn tới. Nhưng để quản lý dễ dàng hơn, tôi sẽ tạo một file có tên tương tự ở thư mục Home. Sau đó ở tệp `urls.py` của mục ToDoList:

```python
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('Home.urls')),
]
```

Khi viết như vậy, những đường dẫn với giá trị `''` nó sẽ đấn đến các đường dẫn ở trong `Home.urls`

Trong tệp `Home/urls.py` sẽ được viết như sau:

```python
from django.urls import re_path as url
from django.urls import path
from .views import ToDoListApiView

urlpatterns = [
    path('api/', ToDoListApiView.as_view()),
]
```

Như vậy khi gọi đến đường dẫn http://127.0.0.1:8000/api thì lớp `ToDoListApiView` trong file views.py sẽ được thực thi.

Tiếp tục với những API khác, tôi sẽ viết một api cho phép get, put, delete một đối tượng có id cụ thể.

```python
class ToDoDetailView(APIView):
    #get mot object ListDo với id cụ thể
    def get (self, request, id):
        try:
            obj = ListDo.objects.get(id=id)
            if (obj.removed==True):
                msg = {"msg": "be removed"}
                return Response(msg)
        except ListDo.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = ToDoListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


    #phương thức put cho phép sửa các giá trị của 1 object với giá trị id cho sẳng
    def put (self, request, id):
        #kiểm tra đối tượng cần sửa có trong database hay không
        try:
            obj = ListDo.objects.get(id=id)
        except ListDo.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = ToDoListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #xóa một đối tượng được chỉ định
    def delete (self, request, id):
        try:
            obj = ListDo.objects.get(id=id)
        except ListDo.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        obj.removed = True
        serializer = ToDoListSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
        obj.save()
        return Response({'msg': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

```

Tương tự nhuư hàm trên thì để gọi được `ToDoDetailView` thực thi ta cũng phải gọi nó trong file `urls.py`

```python
from django.urls import re_path as url
from django.urls import path
from .views import ToDoListApiView, ToDoDetailView

urlpatterns = [
    path('api/<int:id>', ToDoDetailView.as_view()),
    path('api/', ToDoListApiView.as_view()),
]
```

Nhưng khác với `ToDoListApiView`, `ToDoDetailView` cần cung cấp một id đầu vào nên đằng sau đường dẫn chúng ta cần truyền vào một dữ liệu kiểu int là `<int:id>`. Như vậy, sau khi truy cập vào đường link http://127.0.0.1:8000/api/id1 thì sẽ nhận được kết quả trả về là một đối tượng có địa chỉ id là id1.

Sau khi up danh sách các việc cần làm, ở font-end có nhu cầu muốn thay đổi vị trí các việc cần làm, sau khi thay đổi vị trí, giá trị order sẽ đươc font-end thay đổi, việc của tôi cần làm là update các giá trị sau khi thay đổi trên font-end.

Tôi cần viết thêm một class mới ở file `views.py`:

```python
class UpdateOrder(generics.ListCreateAPIView):
    queryset = ListDo.objects.filter(removed=False)
    serializer_class = ToDoListSerializer
    #Sử dụng ListCreateAPIView mà không sử dụng UpdateAPIView vì ListCreateAPIView có hỗ trọ 3 phương thức GET, PUT, POST trong khi đó UpdateAPIView chỉ hỗ trợ phương thức PUT mà không có GET
    #Viết một hàm GET để sau khi sửa dữu liệu dưới database sẽ hỗ trợ load dữ liệu lên font-end
    def get(self, request):
        obj = ListDo.objects.filter(removed=False)
        serializer = ToDoListSerializer(obj, many=True)
        return Response(serializer.data, status=200)

    #Hàm put ở đây dùng để lấy list tất cả các object ListDo đang có trên font-end sau đó ghi đè lên list đang được lưu ở CSDL.
    def put(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instances = list(queryset)
        count = len(instances)
        data = [request.data]
        #in giá trị data get về để kiểm tra giá trị có như mong muốn
        print(data)
        serializer = ToDoListSerializer(instances, data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_list_update(serializer)
        return Response(status=204)

    #Hàm perform_list_update gồn 2 vòng for để ghi đè tất cả giá trị trong list request được lên database.
    def perform_list_update(self, serializer):
        for instance, data in zip(serializer.instance, serializer.validated_data):
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
```

Gọi hàm ở `urls.py` để thực thi:

```python
from django.urls import re_path as url
from django.urls import path
from .views import ToDoListApiView, ToDoDetailView, UpdateOrder

urlpatterns = [
    path('api/<int:id>', ToDoDetailView.as_view()),
    path('api/', ToDoListApiView.as_view()),
    path('api/update', UpdateOrder.as_view()),
]
```

Như vậy api ở http://127.0.0.1:8000/api/update sẽ trả về 2 method là GET và PUT, GET để load dữ liệu và PUT để thay đổi dữ liệu trong database.

Sau khi viết các API cho `ListDo`, tôi sẽ tiến hành viết API cho các `List` với các phương thức GET, POST, PUT, DELETE như `ListDo`

```python
class ListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        obj = List.objects.filter(list_removed=False)
        serializer = ListSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def delete(self, request):
        list_todo = List.objects.all()
        for obj in list_todo:
            obj.list_removed = True
            serializer = ListSerializer(data=obj)
            if serializer.is_valid():
                serializer.save()
            obj.save()
        return Response({'msg': 'all deleted'}, status=status.HTTP_204_NO_CONTENT)
    

class ListDetailView(APIView):
    def get (self, request, id):
        try:
            obj = List.objects.get(id=id)
            if (obj.list_removed==True):
                msg = {"msg": "be removed"}
                return Response(msg)
        except List.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = ListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
    def put (self, request, id):
        try:
            obj = List.objects.get(id=id)
            if (obj.list_removed==True):
                msg = {"msg": "be removed"}
                return Response(msg)
        except List.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = ListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete (self, request, id):
        try:
            obj = List.objects.get(id=id)
            if (obj.list_removed==True):
                msg = {"msg": "be removed"}
                return Response(msg)
        except List.DoesNotExist:
            msg = {"msg": "not found"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        obj.list_removed = True
        serializer = ListSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
        obj.save()
        return Response({'msg': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
```

Tôi cũng viết 2 class, 1 class hỗ trợ cho việc GET, POST, DELETE mà không cần địa chỉ id. Ở API này khi gọi đến hàm DELETE, sẽ thực hiện xóa (`removed`=true) toàn bộ List trong CSDL. 1 class hỗ trợ GET, PUT, DELETE với địa chỉ id đầu vào.

# API

## `http://127.0.0.1:8000/api/`

- GET

output :

```api
[
    {
        "id": 29,
        "order": 1,
        "color_bg": "123",
        "content": "lam viec nha",
        "is_completed": false,
        "created_at": "2023-03-13T07:28:00.221305Z",
        "updated_at": "2023-03-13T07:28:00.221341Z",
        "removed": false,
        "list": 5
    },
    {
        "id": 30,
        "order": 2,
        "color_bg": "345",
        "content": "lau nha",
        "is_completed": false,
        "created_at": "2023-03-13T07:28:14.663467Z",
        "updated_at": "2023-03-13T07:28:14.663500Z",
        "removed": false,
        "list": 5
    }
]
```

- POST

input:

```API
{
    "order":5,
    "color_bg":"aaa",
    "content":"hello",
    "list":5,
}
```

output :

```API
{
    "id": 31,
    "order": 5,
    "color_bg": "aaa",
    "content": "hello",
    "is_completed": false,
    "created_at": "2023-03-13T07:29:31.951608Z",
    "updated_at": "2023-03-13T07:29:31.951650Z",
    "removed": false,
    "list": 5
}
```

- DELETE

output :

```API
{
    "msg": "all deleted"
}
```

sau khi sử dụng phương thức DELETE, sử dụng hàm GET sẽ có kết quả:

```
[]
```

Nhưng nếu chúng ta thay đổi code ở hàm GET từ

```python
obj = ListDo.objects.filter(removed=False)
```

Thành

```python
obj = ListDo.objects.all()
```

Ta sẽ được kết quả là

```json
[
    {
        "id": 29,
        "order": 1,
        "color_bg": "123",
        "content": "lam viec nha",
        "is_completed": false,
        "created_at": "2023-03-13T07:28:00.221305Z",
        "updated_at": "2023-03-13T07:32:25.252335Z",
        "removed": true,
        "list": 5
    },
    {
        "id": 30,
        "order": 2,
        "color_bg": "345",
        "content": "lau nha",
        "is_completed": false,
        "created_at": "2023-03-13T07:28:14.663467Z",
        "updated_at": "2023-03-13T07:32:25.255214Z",
        "removed": true,
        "list": 5
    },
    {
        "id": 31,
        "order": 5,
        "color_bg": "aaa",
        "content": "hello",
        "is_completed": false,
        "created_at": "2023-03-13T07:29:31.951608Z",
        "updated_at": "2023-03-13T07:32:25.257125Z",
        "removed": true,
        "list": 5
    }
]
```

Tức là các object này không bị xóa đi khỏi CSDL mà chỉ gáng biến `removed`=True, và phương thức GET sử dụng filter để lọc ra những đối tượng có biến `removed`=False.

## `http://127.0.0.1:8000/api/<int:id>`

- GET

Phương thức này sẽ GET một đối tượng của một giá trị id cụ thể, ví dụ với http://127.0.0.1:8000/api/27 sẽ trả về output là đối tượng có id 27, nhưng vì ở đây đối tượng có id 27 đã bị xóa nên sẽ trả về:

```json
{
    "msg": "be removed"
}
```

Tương tự nếu GET một đối tượng chưa bị xóa thì kết quả output sẽ là:

```json
{
    "id": 29,
    "order": 1,
    "color_bg": "123",
    "content": "lam viec nha",
    "is_completed": false,
    "created_at": "2023-03-13T07:28:00.221305Z",
    "updated_at": "2023-03-13T07:37:13.842621Z",
    "removed": false,
    "list": 5
}
```

- PUT

Ví dụ ở đây, chúng ta sẽ sửa `color_bg` từ `123` thành `456` object thứ 29, output:

```json
{
    "id": 29,
    "order": 1,
    "color_bg": "456",
    "content": "lam viec nha",
    "is_completed": false,
    "created_at": "2023-03-13T07:28:00.221305Z",
    "updated_at": "2023-03-13T07:39:53.789505Z",
    "removed": false,
    "list": 5
}
```

* DELETE

output:

```json
{
    "msg": "deleted"
}
```

Tương tự như phương thức DELETE ở trên, thì phương thức DELETE ở đây cũng chỉ gáng biến `removed`=False chứ không xóa khỏi CSDL.

## `http://127.0.0.1:8000/api/update`

- Update (PUT)

Hàm Update ở đây chỉ hỗ trợ ghi đè tất cả giá trị mà font-end gửi xuống.

input :

```json
[
    {"id":29,"order":11,"color_bg":"456","content":"lam viec nha","is_completed":false,"created_at":"2023-03-13T07:28:00.221305Z","updated_at":"2023-03-13T07:39:53.789505Z","removed":false,"list":5},
    {"id":31,"order":12,"color_bg":"aaa","content":"hello","is_completed":false,"created_at":"2023-03-13T07:29:31.951608Z","updated_at":"2023-03-13T07:37:13.847465Z","removed":false,"list":5}
]
```

Sau khi sử dụng hàm Update trên, sử dụng hàm GET sẽ cho ra output :

```json
[
    {
        "id": 29,
        "order": 11,
        "color_bg": "456",
        "content": "lam viec nha",
        "is_completed": false,
        "created_at": "2023-03-13T07:28:00.221305Z",
        "updated_at": "2023-03-13T07:42:07.178773Z",
        "removed": false,
        "list": 5
    },
    {
        "id": 31,
        "order": 12,
        "color_bg": "aaa",
        "content": "hello",
        "is_completed": false,
        "created_at": "2023-03-13T07:29:31.951608Z",
        "updated_at": "2023-03-13T07:42:07.181898Z",
        "removed": false,
        "list": 5
    }
]
```
## `http://0.0.0.0:8080/api/list`
* GET

output:

```json
[
    {
        "id": 5,
        "list_create_at": "2023-03-08T06:19:55.453806Z",
        "list_update_at": "2023-03-13T07:45:57.331126Z",
        "list_removed": false,
        "ping": false,
        "list_completed": false
    },
    {
        "id": 9,
        "list_create_at": "2023-03-08T10:15:55.881290Z",
        "list_update_at": "2023-03-08T10:15:55.881329Z",
        "list_removed": false,
        "ping": false,
        "list_completed": false
    }
]
```
* POST

input:

```json
{
    "ping": true,
    "list_completed": false
}
```
output:
```json
{
    "id": 10,
    "list_create_at": "2023-03-13T07:53:23.898468Z",
    "list_update_at": "2023-03-13T07:53:23.898548Z",
    "list_removed": false,
    "ping": true,
    "list_completed": false
}
```
* DELETE

output:
```json
{
    "msg": "all deleted"
}
```
## `http://0.0.0.0:8080/api/list/<int:id>`
* GET: http://0.0.0.0:8080/api/list/9

output:
```json
{
    "id": 9,
    "list_create_at": "2023-03-08T10:15:55.881290Z",
    "list_update_at": "2023-03-08T10:15:55.881329Z",
    "list_removed": false,
    "ping": false,
    "list_completed": false
}
```
GET 1 phần tử đã bị xóa, output:
```json
{
    "msg": "be removed"
}
```
* PUT http://0.0.0.0:8080/api/list/9

input:
```json
{
    "list_completed": true
}
```
output:
```json
{
    "id": 9,
    "list_create_at": "2023-03-08T10:15:55.881290Z",
    "list_update_at": "2023-03-13T08:02:12.003763Z",
    "list_removed": false,
    "ping": false,
    "list_completed": true
}
```
* DELETE http://0.0.0.0:8080/api/list/5

output:
```json
{
    "msg": "deleted"
}
```
# Kết Luận

Project của mình bao gồm các api đơn giản như thêm, xóa, sửa nhưng nó là dự án đầu tiên của mình nên có thể có khá nhiều khó khăn trong việc tìm hiểu và tiếp xúc với công nghệ mới, vì vậy có thể có một vài lỗi không mong muốn, cũng như việc code không được tối ưu. Mình hy vọng mọi người đọc bài viết này có thể để lại một ý kiến để mình có thể sửa lỗi và cải thiện hơn trên con đường theo đuổi django của mình. Cảm ơn và chúc các bạn có một ngày vui vẻ.

link github: https://github.com/ThanhNhan201/List_do.git
