public class ObjThreadProp
{
    public int crawled = 0;
    public int to_crawl = 0;
    public int refused = 0;
    public int dns = 0;

    public void inc_crawled()
    {
        crawled++;
    }

    public void setTo_crawl(int arg)
    {
        to_crawl = arg;
    }

    public void inc_refused()
    {
        refused++;
    }

    public void inc_dns()
    {
        dns++;
    }

}
