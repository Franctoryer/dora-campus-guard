package com.franctoryer.dora.graphql;

import com.franctoryer.dora.vo.Mark;
import com.franctoryer.dora.vo.UserDetail;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.graphql.data.method.annotation.SchemaMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
public class UserResolver {
    @QueryMapping
    public UserDetail getUserDetailById(@Argument Long id) {
        return new UserDetail(100L, "Franctoryer", 23, 1701291281);
    }

    @SchemaMapping(typeName = "UserDetail", field = "marks")
    public List<Mark> marks(@Argument UserDetail userDetail) {
        return List.of(new Mark(1, 3.11F), new Mark(2, 3.89F));
    }
}
