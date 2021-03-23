SELECT "taskorgapi_tags"."id", "taskorgapi_tags"."label",
        "taskorgapi_tags"."author_id" 
 FROM "taskorgapi_tags" 
 INNER JOIN "taskorgapi_tasktags" 
 ON ("taskorgapi_tags"."id" = "taskorgapi_tasktags"."tag_id") 
 WHERE "taskorgapi_tasktags"."task_id" = 1