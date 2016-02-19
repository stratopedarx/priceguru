SELECT
        "ItemPrice"."created_date",
        "ItemPrice"."current_price",
        "ItemPrice"."currency",
        "OriginalItem"."title",
        "ItemGroup"."group_name"
from "ItemPrice"
        LEFT JOIN "OriginalItem" ON "ItemPrice"."item_id"="OriginalItem"."id"
        LEFT JOIN "UserItem" ON "UserItem"."item_id"="OriginalItem"."id"
        LEFT JOIN "ItemGroup" ON "ItemGroup"."id"="UserItem"."group_id"
 WHERE
        "UserItem"."group_id" IN (SELECT "ItemGroup"."id" FROM "ItemGroup" ORDER BY random() LIMIT 3)
        AND
        "ItemPrice"."created_date" > now() - interval '2 days'
ORDER BY "ItemGroup"."group_name", "OriginalItem"."title", "ItemPrice"."created_date";
