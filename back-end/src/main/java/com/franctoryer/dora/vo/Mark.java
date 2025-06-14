package com.franctoryer.dora.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Mark {
    // 主键
    private Integer semester;

    // 绩点
    private Float gpa;
}
