public class ShutdownThread extends Thread
{

    private IShutdownThreadParent mShutdownThreadParent;

    public ShutdownThread(IShutdownThreadParent mShutdownThreadParent)
    {
        this.mShutdownThreadParent = mShutdownThreadParent;
    }

    @Override
    public void run()
    {
        this.mShutdownThreadParent.shutdown();
    }
}
