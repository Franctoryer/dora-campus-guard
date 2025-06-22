package com.franctoryer.dora.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.franctoryer.dora.entity.Post;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface PostMapper extends BaseMapper<Post> {
}
