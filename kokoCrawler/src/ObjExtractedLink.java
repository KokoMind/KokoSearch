public class ObjExtractedLink
{
    public ObjLink link;
    public ObjLinkProp prop;

    public ObjExtractedLink(ObjLink link, ObjLinkProp prop)
    {
        this.link = link;
        this.prop = prop;
    }

    public ObjExtractedLink(ObjLink link, int out_links, int sz_parent, double parent_priority)
    {
        this.link = link;
        this.prop = new ObjLinkProp(out_links, sz_parent, link.url.length(), parent_priority);
    }

    public static ObjExtractedLink[] setup_extracted_links(ObjLink[] links, int sz_content, double priority)
    {
        ObjExtractedLink ret[] = new ObjExtractedLink[links.length];
        int sz = links.length;
        for (int i = 0; i < sz; i++)
        {
            ret[i] = new ObjExtractedLink(links[i], sz, sz_content, priority);
        }
        return ret;
    }
}
