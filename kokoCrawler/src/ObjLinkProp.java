public class ObjLinkProp
{
    public int out_links;
    public int sz_parent;
    public int sz_url;
    public double parent_priority;

    public ObjLinkProp(int out_links, int sz_parent, int sz_url, double parent_priority)
    {
        this.out_links = out_links;
        this.sz_parent = sz_parent;
        this.sz_url = sz_url;
        this.parent_priority = parent_priority;
    }
}
