post_spider_config = {
    "fields": [
        {
            "name": "id",
            "path": "data.posts[*].id",
            "description": "帖子 ID"
        },
        {
            "name": "content",
            "path": "data.posts[*].name",
            "description": "帖子正文"
        },
        {
            "name": "uid",
            "path": "data.posts[*].user.id",
            "description": "发帖者 ID"
        },
        {
            "name": "is_anonymous",
            "path": "data.posts[*].majia",
            "description": "是否匿名发帖"
        },
        {
            "name": "is_distinguished",
            "path": "data.posts[*].jinghua",
            "description": "是否精选"
        },
        {
            "name": "picture_urls",
            "path": "data.posts[*].myimages",
            "description": "图片 url"
        },
        {
            "name": "topic_id",
            "path": "data.posts[*].topic_id",
            "description": "话题 ID"
        },
        {
            "name": "comment_sum",
            "path": "data.posts[*].commentsum",
            "description": "评论数"
        },
        {
            "name": "like_sum",
            "path": "data.posts[*].zansum",
            "description": "点赞数"
        },
        {
            "name": "hot",
            "path": "data.posts[*].hot",
            "description": "热度"
        },
        {
            "name": "tip_sum",
            "path": "data.posts[*].jubaocount",
            "description": "举报数"
        },
        {
            "name": "forward_sum",
            "path": "data.posts[*].sharenum",
            "description": "转发数"
        },
        {
            "name": "published_at",
            "path": "data.posts[*].createtime",
            "description": "发布时间"
        },
        {
            "name": "is_ever_top",
            "path": "data.posts[*].top",
            "description": "是否曾经置顶"
        },
        {
            "name": "ever_top_end_time",
            "path": "data.posts[*].topEndTime",
            "description": "曾经置顶的结束时间"
        },
    ]

}

user_spider_config = {
    "fields": [
        {
            "name": "uid",
            "path": "data.posts[*].user.id",
            "description": "用户 ID"
        },
        {
            "name": "avatar_url",
            "path": "data.posts[*].user.avatar",
            "description": "头像地址"
        },
        {
            "name": "gender",
            "path": "data.posts[*].user.gender",
            "description": "性别"
        },
        {
            "name": "level",
            "path": "data.posts[*].user.level",
            "description": "等级"
        },
        {
            "name": "nickname",
            "path": "data.posts[*].user.nickname",
            "description": "昵称"
        },
        {
            "name": "is_admin",
            "path": "data.posts[*].user.isAdmin",
            "description": "是否是管理员"
        },
        {
            "name": "dora_value",
            "path": "data.posts[*].user.dlzs",
            "description": "哆啦值"
        },
        {
            "name": "dora_coin",
            "path": "data.posts[*].user.doracoin",
            "description": "哆啦币"
        },
        {
            "name": "likes",
            "path": "data.posts[*].user.likes",
            "description": "被哪些人关注？（暂时未知）"
        },
        {
            "name": "hide_permission",
            "path": "data.posts[*].user.nohidepermission",
            "description": "是否隐藏主页"
        },
        {
            "name": "is_anonymous",
            "path": "data.posts[*].majia",
            "description": "是否匿名"
        },
    ]
}