package com.franctoryer.dora.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.franctoryer.dora.entity.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper extends BaseMapper<User> {
}
