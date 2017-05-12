import java.io.IOException;

public class Crawl
{

    // Mode 0 - init   ,  Mode 1 - cont   ,  Mode 2 - revisit
    public int mode;
    public int num_workers;
    public String tocrawl_db_name = null;
    public int port_number;


    public void run()
    {
        Controller crawler_CEO = new Controller(num_workers, seeds, mode, port_number, tocrawl_db_name);
        crawler_CEO.run();
    }

    public Crawl(String[] args) throws IOException
    {
        if (check_args(args) == -1)
            throw new IOException();
        System.out.println("Arguments are parsed successfully and we are Ready to crawl");
    }

    public int check_args(String[] args)
    {
        String firstArg;
        int secondArg;
        if (args.length >= 2)
        {
            try
            {
                boolean validFirstArg = false;
                secondArg = Integer.parseInt(args[1]);
                for (String s : moods)
                {
                    if (s.equals(args[0]))
                        validFirstArg = true;
                }
                if (!validFirstArg)
                    return -1;
                if (args[0].equals("cont") && args.length < 3)
                    return -1;

                if (args[0].equals("init"))
                {
                    mode = 0;
                    port_number = Integer.parseInt(args[2]);
                }
                else if (args[0].equals("cont"))
                {
                    mode = 1;
                    tocrawl_db_name = args[2];
                }
                num_workers = secondArg;
            }
            catch (NumberFormatException e)
            {
                System.err.println("Argument" + args[1] + " must be an integer.");
                return -1;
            }
        }
        else
        {
            return -1;
        }
        return 0;
    }

    public String moods[] = {
            "init",
            "cont",
            "revisit"
    };

    public String seeds[] = {
            "https://en.wikipedia.org",
            "http://www.W3.org",
            "http://web.mit.edu",
            "http://stanford.edu",
            "https://www.rottentomatoes.com",
            "http://www.imdb.com",
            "http://screenrant.com",
            "https://vimeo.com",
            "http://www.100bestwebsites.org",
            "http://www.makeuseof.com/tag/best-websites-internet",
            "https://moz.com/top500",
            "https://www.bloomberg.com",
            "https://www.reddit.com/r/Futurology/comments/48b5oc/best_of_2015_winners",
            "https://moz.com/blog",
            "http://www.berkeley.edu",
            "https://www.cam.ac.uk",
            "http://www.ox.ac.uk",
            "http://www.caltech.edu",
            "http://www.dmoz.org",
            "http://www.ebay.com",
            "https://www.cnet.com",
            "https://www.spotify.com",
            "https://archive.org",
            "http://www.ieee.org",
            "http://www.nike.com",
            "https://en-maktoob.yahoo.com",
    };
}
