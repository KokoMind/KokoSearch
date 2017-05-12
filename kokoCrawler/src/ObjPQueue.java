public class ObjPQueue implements Comparable<ObjPQueue>
{
    public String url;
    public String dns;
    public double value;

    public ObjPQueue(String url, String dns, double val)
    {
        this.url = url;
        this.dns = dns;
        this.value = val;
    }

    public int compareTo(ObjPQueue other)
    {
        return Double.compare(other.value, this.value);
    }
}
