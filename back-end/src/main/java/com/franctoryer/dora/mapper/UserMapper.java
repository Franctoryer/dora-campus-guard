package com.franctoryer.dora.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.franctoryer.dora.entity.User;
import com.franctoryer.dora.vo.post.PostUserVo;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    List<PostUserVo> getDetailByUids(List<Long> uids);
}
