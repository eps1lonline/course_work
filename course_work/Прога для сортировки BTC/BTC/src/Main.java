import java.io.IOException;
import java.io.FileWriter;
import java.util.Scanner;
import java.io.File;

public class Main {
    public static void main(String[] args) throws IOException {
        Scanner scan = new Scanner(new File("USD_Month.txt"));
        FileWriter fw = new FileWriter(new File("USD_Corrected_Month.txt"));

        /*Scanner scan = new Scanner(new File("BTC_Weekly.txt"));
        FileWriter fw = new FileWriter(new File("BTC_Corrected_Weekly.txt"));*/

        /*Scanner scan = new Scanner(new File("BTC_Month.txt"));
        FileWriter fw = new FileWriter(new File("BTC_Corrected_Month.txt"));*/

        String str;
        String[] mass = new String[512];
        Integer strCount = 0;

        while (scan.hasNextLine()) {
            String ptr = scan.nextLine();

            String data = ptr.substring(0, ptr.indexOf("\t"));
            str = data.substring(data.lastIndexOf(".") + 1, data.length()) + "-"; // year
            str += data.substring(data.indexOf(".") + 1, data.lastIndexOf(".")) + "-"; // month
            str += data.substring(0, data.indexOf(".")); // day

            ptr = ptr.substring(ptr.indexOf("\t") + 1, ptr.length());

            String value = ptr.substring(0, ptr.indexOf("\t") - 2);
            value = value.replace(".", "");

            str += "    " + value + "\n";
            mass[strCount] = str;
            strCount++;
        }
        System.out.println("Кол-во строк: " + strCount);

        for (int i = strCount - 1; i > 0 ; i--) {
            System.out.println(mass[i]);
            fw.write(mass[i]);
        }

        scan.close();
        fw.close();
    }
}