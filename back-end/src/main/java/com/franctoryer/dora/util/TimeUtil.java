package com.franctoryer.dora.util;

import co.elastic.clients.elasticsearch._types.aggregations.CalendarInterval;

public class TimeUtil {
    public static CalendarInterval convertStrToCalendar(String str) {
        if (str == null || str.isBlank()) {
            throw new IllegalArgumentException("时间间隔不能为空");
        }

        return switch (str.toLowerCase()) {
            case "second" -> CalendarInterval.Second;
            case "minute" -> CalendarInterval.Minute;
            case "hour" -> CalendarInterval.Hour;
            case "day" -> CalendarInterval.Day;
            case "week" -> CalendarInterval.Week;
            case "month" -> CalendarInterval.Month;
            case "quarter" -> CalendarInterval.Quarter;
            case "year" -> CalendarInterval.Year;
            default -> throw new IllegalArgumentException("不支持的时间间隔: " + str);
        };
    }
}
