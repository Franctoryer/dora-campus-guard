package com.franctoryer.dora.dto.post;

import jakarta.validation.constraints.Max;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PostContentSearchDto {
    @Length(max = 50, message = "关键词不能超过 50 个字符")
    private String keyword;

    private Integer page;

    @Max(value = 40, message = "每页数量不能超过 40")
    private Integer size;
}
