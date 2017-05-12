import com.mongodb.*;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

import static com.mongodb.client.model.Filters.*;
import static com.mongodb.client.model.Updates.*;

import com.mongodb.client.model.UpdateOptions;
import com.mongodb.client.result.*;
import org.bson.Document;
import org.bson.types.ObjectId;


import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;


public class MongoTest
{
    public static void main(String[] args)
    {
        MongoClient mongoClient = new MongoClient(new ServerAddress("localhost", 27018));

        MongoDatabase db = mongoClient.getDatabase("crawled");

        MongoCollection<Document> crawled_col = db.getCollection("crawled");

        for (String name : db.listCollectionNames())
        {
            System.out.println(name);
        }

        List<Document> documents = new ArrayList<Document>();

        for (int i = 0; i < 100; i++)
        {
            ObjPage p = new ObjPage("www", "dnsdns", "5lty", 1);
            documents.add(p.record);
        }

        crawled_col.insertMany(documents);

        mongoClient.close();
    }
}
