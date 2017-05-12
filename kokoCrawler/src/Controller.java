public class Controller implements IShutdownThreadParent
{

    public int num_workers;
    public Worker workers[];
    public WorkerSaver saver;
    public Frontier frontier;
    public DB db;
    public Dashboard dash;
    private volatile boolean keepOn = true;

    private ShutdownThread fShutdownThread;


    public Controller(int num_threads, String[] seeds, int mode, int port_no, String to_crawl_db_name)
    {
        num_workers = num_threads;
        workers = new Worker[num_threads];
        dash = new Dashboard();
        db = new DB(port_no);
        frontier = new Frontier(num_threads, db, dash);

        for (int i = 0; i < num_workers; i++)
        {
            workers[i] = new Worker(i, "Thread-" + String.valueOf(i), frontier, db, dash);
        }
        saver = new WorkerSaver(-1, "Thread-Saver", frontier, dash, port_no);
        System.out.println("Workers Created");

        if (mode == 0) // Mode init
        {
            ObjExtractedLink links[] = setup_seeds(seeds);
            frontier.distribute_seeds(links);
            System.out.println("Seeds distributed");
        }
        else if (mode == 1) //Mode cont
        {
            frontier.load_to_crawl(to_crawl_db_name, null);
        }
        //For interrupt
        fShutdownThread = new ShutdownThread(this);
        Runtime.getRuntime().addShutdownHook(fShutdownThread);
    }

    @Override
    public void shutdown()
    {
        // code to cleanly shutdown my Controller.
        try
        {
            for (int i = 0; i < num_workers; i++)
                workers[i].join();
            saver.join();
            System.out.println("All Workers Exit");
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        finally
        {
            frontier.save_to_crawl();
            System.out.println("Saved EL7");
        }
    }

    public void run()
    {
        try
        {
            for (int i = 0; i < num_workers; i++)
                workers[i].start();
            saver.start();

            frontier.distribute();

            for (int i = 0; i < num_workers; i++)
                workers[i].join();
            saver.join();
            System.out.println("All Workers Exit");
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        finally
        {
            frontier.save_to_crawl();
            System.out.println("Saved EL7");
        }
    }

    public ObjExtractedLink[] setup_seeds(String[] seeds)
    {
        System.out.println("Setting the Seeds");
        ObjLink links[] = new ObjLink[seeds.length];
        int sz = seeds.length;
        for (int i = 0; i < sz; i++)
        {
            links[i] = new ObjLink(seeds[i], Fetcher.extractDNS(seeds[i]));
        }
        ObjExtractedLink ret[] = new ObjExtractedLink[links.length];
        for (int i = 0; i < sz; i++)
        {
            ret[i] = new ObjExtractedLink(links[i], 100000, 100000, 1);
        }
        System.out.println("Seeds are ready");
        System.out.println("Number of seeds = " + String.valueOf(ret.length));
        return ret;
    }
}
