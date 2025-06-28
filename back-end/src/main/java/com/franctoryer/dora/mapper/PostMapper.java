package com.franctoryer.dora.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.franctoryer.dora.entity.Post;
import com.franctoryer.dora.vo.detection.DetectionPostListVo;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface PostMapper extends BaseMapper<Post> {
    IPage<DetectionPostListVo> selectDetectionPostPage(
            Page<DetectionPostListVo> page,
            Integer abnormalIndex
    );
}
