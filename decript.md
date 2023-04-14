
# API
## api truyen chu: `http://127.0.0.1:8000/api/comics/chap/image/382`
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

