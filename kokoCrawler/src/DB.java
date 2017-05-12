import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import com.mongodb.MongoClient;
import com.mongodb.MongoException;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.apache.commons.codec.digest.DigestUtils;
import org.bson.Document;

public class DB
{

    private int port_no;

    public DB(int no)
    {
        port_no = no;
    }

    public int cache_to_crawl(ObjPQueue[][] arr)
    {
        try
        {
            MongoClient mongoClient = new MongoClient(new ServerAddress("localhost", port_no));

            MongoDatabase db = mongoClient.getDatabase("tocrawl");

            MongoCollection<Document> crawled_col = db.getCollection("tocrawl" + String.valueOf(System.currentTimeMillis()));

            System.out.println("MONGOOO RRRRRRRRAAAAAAAAAHHHHHHHH");

            List<Document> documents = new ArrayList<Document>();

            for (ObjPQueue[] array : arr)
            {
                for (ObjPQueue link : array)
                {
                    Document record = new Document();
                    record.put("url", link.url);
                    record.put("dns", link.dns);
                    record.put("value", String.valueOf(link.value));
                    documents.add(record);
                }
            }

            crawled_col.insertMany(documents);

            mongoClient.close();

            return 0;
        }
        catch (MongoException e)
        {
            e.printStackTrace();
            return -1;
        }
    }

    public ArrayList<ObjPQueue> get_to_crawl(String name, Integer num)
    {
        return null;
    }
}
