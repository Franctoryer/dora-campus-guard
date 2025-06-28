/**
 * 情感分布返回值
 */
export interface SentimentDistribution {
  /**
   * 标签 ID
   */
  labelId: number

  /**
   * 标签名称
   */
  labelName: string

  /**
   * 统计数
   */
  count: number
}

/**
 * 讨论趋势返回值
 */
export interface keywordTrend {
  /**
   * 时间
   */
  dateTime: string

  /**
   * 讨论热度
   */
  count: number
}
