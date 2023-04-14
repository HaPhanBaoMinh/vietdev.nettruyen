
# API
## api doc truyen chu: `http://127.0.0.1:8000/api/comics/chap/image/382`
* GET

output:

```json
{
    "id": 2,
    "chap": {
        "id": 382,
        "name": "Chương 2: Tuyệt, hắn tán thành hôn sự này!"
    },
    "content": "Hiện giờ Trương Nguyệt Nhi quản lý hậu viện nên Liễu Ngọc Như muốn ra ngoài cần được Trương Nguyệt Nhi cho phép.\r\n\r\nẤn Hồng không hiểu vì sao Liễu Ngọc Như lại dặn bảo như vậy, chỉ đành nhắc nhở, “Tiểu thư trước hết hẳn nên báo với phu nhân chuyện hôn sự này?”\r\n\r\n...",
    "is_novel": true
}
```
## api get comic by author `http://127.0.0.1:8000/api/comics/author/`

* GET

input:
```json
{
    "author": "Chidori Komatsubara"
}
```

output
```json
[
    {
        "image": "/nettruyen/media/comic/nguoi-dep-hoa-ra-la-quai-vat-chang-trai-thanh-thi-va-co-gai-pho-thi.jpg",
        "name": "Người Đẹp Hóa Ra Là Quái Vật? Chàng Trai Thành Thị Và Cô Gái Phố Thị",
        "newest_chap": [
            {
                "chap_num": 1,
                "name": "Chap 1",
                "created_at": "2023-03-31T01:33:03.110000Z"
            },
            {
                "chap_num": 2,
                "name": "Chap 2",
                "created_at": "2023-03-31T01:33:03.110000Z"
            },
            {
                "chap_num": 3,
                "name": "Chap 3",
                "created_at": "2023-03-31T01:33:03.110000Z"
            }
        ],
        "genres": [
            {
                "name": "Drama",
                "slug": "drama"
            },
            {
                "name": "Ecchi",
                "slug": "ecchi"
            },
            {
                "name": "Gender Bender",
                "slug": "gender-bender"
            },
            {
                "name": "Josei",
                "slug": "josei"
            },
            {
                "name": "Mature",
                "slug": "mature"
            },
            {
                "name": "Romance",
                "slug": "romance"
            },
            {
                "name": "Shoujo",
                "slug": "shoujo"
            },
            {
                "name": "Smut",
                "slug": "smut"
            }
        ]
    }
]
```

## api theo dõi khi là khách: `http://127.0.0.1:8000/api/users/follow_anonymous`

* POST

input: 
```json
{
    "comic_id": "50"
}
```

output
```json
{
    "followed": true
}
```
* GET

output
```json
[
    {
        "image": "/nettruyen/media/comic/ket-thuc-nhat-dinh-se-co-hau.jpg",
        "name": "Kết Thúc Nhất Định Sẽ Có Hậu",
        "newest_chap": [
            {
                "chap_num": 1,
                "name": "Chap 1",
                "created_at": "2023-03-31T01:33:03.110000Z"
            },
            {
                "chap_num": 2,
                "name": "Chap 2",
                "created_at": "2023-03-31T01:33:03.110000Z"
            },
            {
                "chap_num": 3,
                "name": "Chap 3",
                "created_at": "2023-03-31T01:33:03.110000Z"
            }
        ],
        "genres": [
            {
                "name": "Manhwa",
                "slug": "manhwa"
            },
            {
                "name": "Ngôn Tình",
                "slug": "ngon-tinh"
            },
            {
                "name": "Romance",
                "slug": "romance"
            },
            {
                "name": "Truyện Màu",
                "slug": "truyen-mau"
            }
        ]
    },
]
```

## api theo dõi khi là user `http://127.0.0.1:8000/api/users/follow`
* GET

output:
```json
[
    {
        "comic": {
            "image": "/nettruyen/media/comic/truong-phong-do.png",
            "name": "Trường Phong Độ",
            "newest_chap": [
                {
                    "chap_num": 3,
                    "name": "Chương 3: Không phải bảo gả cho ta sẽ lập tức nhảy hồ Sao?",
                    "created_at": "2023-04-13T09:37:08.086638Z"
                },
                {
                    "chap_num": 2,
                    "name": "Chương 2: Tuyệt, hắn tán thành hôn sự này!",
                    "created_at": "2023-04-13T08:41:00.705946Z"
                },
                {
                    "chap_num": 1,
                    "name": "Chap 1: Đính hôn",
                    "created_at": "2023-04-13T08:27:24.211321Z"
                }
            ],
            "genres": [
                {
                    "name": "Cổ Đại",
                    "slug": "co-dai"
                }
            ]
        },
        "readed": false
    }
]
```
* POST
input: 
```json
{
    "comic_id": "50"
}
```
output:
```json
{
    "message": "Success!"
}
```

## api đồng bộ hóa follow khi user đăng nhập `http://127.0.0.1:8000/api/users/follow_sync`

* POST

output
```json
{
    "msg": "list follow updated"
}
```

