import org.bson.Document;

import java.time.LocalDateTime;

public class ObjPage
{
    Document record;

    public ObjPage(String url, String dns, String content, int thread_id)
    {
        record = new Document();
        record.put("url", url);
        record.put("dns", dns);
        record.put("thread_id", thread_id);
        record.put("visited", LocalDateTime.now().toString());
        record.put("indexed", "false");
        record.put("content", content);
    }
}
