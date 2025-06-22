post_list_config = {
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

post_detail_config = {
    "fields": [
        {
            "name": "id",
            "path": "data.postDtl.id",
            "description": "帖子 ID"
        },
        {
            "name": "content",
            "path": "data.postDtl.name",
            "description": "帖子正文"
        },
        {
            "name": "uid",
            "path": "data.postDtl.user.id",
            "description": "发帖者 ID"
        },
        {
            "name": "is_anonymous",
            "path": "data.postDtl.majia",
            "description": "是否匿名发帖"
        },
        {
            "name": "is_distinguished",
            "path": "data.postDtl.jinghua",
            "description": "是否精选"
        },
        {
            "name": "picture_urls",
            "path": "data.postDtl.myimages",
            "description": "图片 url"
        },
        {
            "name": "topic_id",
            "path": "data.postDtl.topic_id",
            "description": "话题 ID"
        },
        {
            "name": "comment_sum",
            "path": "data.postDtl.commentsum",
            "description": "评论数"
        },
        {
            "name": "like_sum",
            "path": "data.postDtl.zansum",
            "description": "点赞数"
        },
        {
            "name": "hot",
            "path": "data.postDtl.hot",
            "description": "热度"
        },
        {
            "name": "tip_sum",
            "path": "data.postDtl.jubaocount",
            "description": "举报数"
        },
        {
            "name": "forward_sum",
            "path": "data.postDtl.sharenum",
            "description": "转发数"
        },
        {
            "name": "published_at",
            "path": "data.postDtl.createtime",
            "description": "发布时间"
        },
        {
            "name": "is_ever_top",
            "path": "data.postDtl.top",
            "description": "是否曾经置顶"
        },
        {
            "name": "ever_top_end_time",
            "path": "data.postDtl.topEndTime",
            "description": "曾经置顶的结束时间"
        },
        {
            "name": "risky",
            "path": "data.postDtl.risky",
            "description": "是否有风险"
        },
        {
            "name": "school_id",
            "path": "data.postDtl.school_id",
            "description": "学校 id"
        },
        {
            "name": "is_fee",
            "path": "data.postDtl.isfee",
            "description": "是否收费"
        },
        {
            "name": "origin",
            "path": "data.postDtl.origin",
            "description": "来源"
        },
        {
            "name": "ad_level",
            "path": "data.postDtl.adlevel",
            "description": "广告等级"
        },
        {
            "name": "settled",
            "path": "data.postDtl.settleed",
            "description": "是否已经解决"
        },
        {
            "name": "dun_num",
            "path": "data.postDtl.dunnum",
            "description": "蹲数"
        },
    ]

}

user_info_config = {
    "fields": [
        {
            "name": "uid",
            "path": "data.postDtl.user.id",
            "description": "用户 ID"
        },
        {
            "name": "avatar_url",
            "path": "data.postDtl.user.avatar",
            "description": "头像地址"
        },
        {
            "name": "gender",
            "path": "data.postDtl.user.gender",
            "description": "性别"
        },
        {
            "name": "level",
            "path": "data.postDtl.user.level",
            "description": "等级"
        },
        {
            "name": "nickname",
            "path": "data.postDtl.user.nickname",
            "description": "昵称"
        },
        {
            "name": "is_admin",
            "path": "data.postDtl.user.isAdmin",
            "description": "是否是管理员"
        },
        {
            "name": "dora_coin",
            "path": "data.postDtl.user.doracoin",
            "description": "哆啦币"
        },
        {
            "name": "hide_permission",
            "path": "data.postDtl.user.nohidepermission",
            "description": "是否隐藏主页"
        },
        {
            "name": "is_anonymous",
            "path": "data.postDtl.majia",
            "description": "是否匿名"
        },
        {
            "name": "school_id",
            "path": "data.postDtl.user.scId",
            "description": "所属学校"
        },
        {
            "name": "eat_tip",
            "path": "data.postDtl.user.eattip",
            "description": "是否被举报"
        }
    ]
}