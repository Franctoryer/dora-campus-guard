class SentimentUtil {
  /**
   *  将标签 ID 转换为标签名称
   * @param labelId 标签 ID
   * @returns
   */
  static getLabelNameFromLabelId(labelId: number): string {
    const labelMap: Record<number, string> = {
      0: '悲伤',
      1: '失望',
      2: '讨厌',
      3: '平和',
      4: '疑惑',
      5: '开心',
      6: '期待',
    }

    return labelMap[labelId] ?? '未知情感'
  }

  /**
   * 获取标签颜色
   * @param labelId 标签 ID
   */
  static getLabelColorFromLabelId(labelId: number): string {
    const colorMap: Record<number, string> = {
      0: 'blue',
      1: 'geekblue',
      2: 'purple',
      3: 'lime',
      4: 'warning',
      5: 'gold',
      6: 'orange',
    }

    return colorMap[labelId] ?? 'error'
  }
}

export default SentimentUtil
