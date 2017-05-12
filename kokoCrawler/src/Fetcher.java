import java.io.UnsupportedEncodingException;
import java.net.*;
import java.nio.charset.Charset;
import java.util.ArrayList;

import com.shekhargulati.urlcleaner.UrlCleaner;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import com.trigonic.jrobotx.RobotExclusion;

public class Fetcher {
    /* Class that will fetch the page, validate that it is of type HTML, extract its contents and hyperlinks */

    private static boolean internetOn() {
        for (int i = 0; i < 5; i++) {
            try {
                URL url = new URL("https://www.google.com/");
                URLConnection connection = url.openConnection();
                connection.connect();
                return true;
            } catch (Exception e) {
            }
        }
        return false;
    }

    private static boolean checkRobots(String url) {
        /* Check that our crawler satisfies robot exclusion standard */
        try {
            URL urll = new URL(url);
            RobotExclusion robotExclusion = new RobotExclusion();
            return robotExclusion.allows(urll,"*");
        } catch (Exception e) {
            return true;
        }
    }

    private static boolean checkURL(String url) {
        /* Checks that URL is alive and of has a response of type html. */
        while (true) {
            try {
                URL urll = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) urll.openConnection();
                connection.setRequestMethod("GET");
                connection.connect();
                if (connection.getResponseCode() == 200) {
                    String contentType = connection.getHeaderField("content-type");
                    return contentType.contains("html");
                } else return false;

            } catch (Exception e) {
                if (Fetcher.internetOn())
                    return false;
                System.out.print("\rConnection lost. Retry!!");
            }
        }
    }

    public static String extractDNS(String url) {
        try {
            InetAddress address = InetAddress.getByName(new URL(url).getHost());
            return address.getHostAddress();
        } catch (Exception e) {
            return null;
        }
    }

    private static boolean checkExtHTML(String url) throws MalformedURLException {
        /* Check the filename extension either HTML or "" */
        URL urll = new URL(url);
        String extension = Fetcher.getURLExtension(urll.getPath());
        String[] targets = {".htm", ".html", ".php", ".aspx", ""};
        for (String target : targets) {
            if (extension.equals(target))
                return true;
        }
        return false;
    }

    private static String getURLExtension(String url) {
        /* Get the extension of the url: .html, .pdf ..etc. */
        String sep = "/", extsep = ".";
        int sepIndex = url.lastIndexOf(sep);
        int dotIndex = url.lastIndexOf(extsep);
        if (dotIndex > sepIndex) {   //skip all leading dots
            int filenameIndex = sepIndex + 1;
            while (filenameIndex < dotIndex) {
                if (!(url.substring(filenameIndex, filenameIndex + 1).equals(extsep))) {
                    return url.substring(dotIndex);

                }
                filenameIndex += 1;
            }
        }
        return "";
    }

    private static Document downloadPage(String url) {
        if (Fetcher.checkURL(url) && Fetcher.checkRobots(url)) {
            try {
                return Jsoup.connect(url).get();
            } catch (Exception e) {
                return null;
            }
        }
        return null;
    }

    private static String extractASCIIOnly(String data) throws UnsupportedEncodingException {
        data = new String(Charset.forName("ascii").encode(data).array(), "ascii");
        data = data.replace('?', ' ');
        return data;
    }

    public static ObjDownloaded fetch(String url) {
        try {
            int threshold = 10;         //To accept a document, it must has length >= threshold
            Document soup = Fetcher.downloadPage(url);
            if (soup == null)
                return null;
            String content = Fetcher.extractContent(soup);
            if (content.length() < threshold)
                return null;
            ArrayList<ObjLink> linksArr = extractLinks(soup);
            ObjLink[] links = new ObjLink[linksArr.size()];
            links = linksArr.toArray(links);
            return new ObjDownloaded(links, content);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private static ArrayList<ObjLink> extractLinks(Document soup) throws MalformedURLException {
        Elements links = soup.select("a");
        ArrayList<ObjLink> stringLinks = new ArrayList<>();
        for (Element link : links) {
            try {
                String absHref = link.attr("abs:href"); // "http://jsoup.org/
                String normalizedURL = UrlCleaner.normalizeUrl(absHref);
                if (Fetcher.checkExtHTML(normalizedURL))
                    stringLinks.add(new ObjLink(normalizedURL, Fetcher.extractDNS(normalizedURL)));
            }
            catch(Exception e) {}
        }
        return stringLinks;
    }


    private static String extractContent(Document soup) throws UnsupportedEncodingException {
        return extractASCIIOnly(soup.text()).trim().replaceAll(" +", " ");
    }

    //public static void main(String[] args){
  //      Fetcher.fetch("https://en.wikipedia.org");
   // }
}
