package com.example.startagain;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {
    private ToggleButton toggleButton;
    private Button closeButton;
    private TextView lightSwitch;
    private TextView tempDisplay;
    private TextView humDisplay;
    private TextView co2Display;
    private TextView methaneDisplay;
    public int state_track = 0;

    public static PrintWriter output;
    public static BufferedReader input;
    Thread listenThread = null;
   // public static Thread send_thread = new Thread(new SendThread());
    public static String SERVER_IP = "192.168.0.34";
    public static final int SERVER_PORT = 8080;
    public static String recvd = "";
    Socket recvSocket;

    class listenThread implements Runnable {
        @Override
        public void run() {
            try {
                recvSocket = new Socket(SERVER_IP, SERVER_PORT);
                System.out.println(state_track);
                state_track = 2;
                try {
                    //recieve messages
                    input = new BufferedReader(new InputStreamReader(recvSocket.getInputStream()));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            while(true){
                try {
                    TimeUnit.SECONDS.sleep(4);
                    System.out.println(state_track);
                    System.out.println(input.ready());
                    if(input.ready() == true){
                      System.out.println(input.readLine());
                    }
                    String read = input.readLine();
                    System.out.println(read);
                    if (read != null) {
                        recvd = read;
                        System.out.println("Received msg");
                        System.out.println(recvd);
                    }
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public void ListenData (){
        System.out.println("In ListenData Method");
        listenThread l = new listenThread();
        System.out.println("L thread Made");
        System.out.println("About to receieve data to thread");
        new Thread(l).start();
    }


    public static void SendData (String data){
        System.out.println("In SendData Method");
        SendThread t = new SendThread();
        System.out.println("T thread Made");
        t.data = data;
        System.out.println("About to send data to thread");
        new Thread(t).start();
    }

    static class SendThread implements Runnable{
        public String data;
        Socket sendSocket;

        @Override
        public void run() {
            try {
                System.out.println("Making Send Socket");
                sendSocket = new Socket(SERVER_IP, SERVER_PORT);
                output =  new PrintWriter(sendSocket.getOutputStream());
                System.out.println("Send Socket MADE");
            } catch (IOException e) {
                e.printStackTrace();
            }
            try {
                System.out.println("In SendThread Method, about to send data to server");
                System.out.println(data);
                output.write(data);
                output.flush();
            }catch (NullPointerException e){
                e.printStackTrace();
            }

        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tempDisplay = (TextView)findViewById(R.id.temp);
        humDisplay = (TextView)findViewById(R.id.hum);
        co2Display = (TextView)findViewById(R.id.co2);
        methaneDisplay = (TextView)findViewById(R.id.methane);
        lightSwitch = (TextView)findViewById(R.id.ls) ;
        int counter = 0;
        System.out.println(state_track);
        state_track = 1;
        ListenData();

        while (counter != 5) {
            SendData("Hello!");
            counter = counter +1;
            try {
                TimeUnit.SECONDS.sleep(4);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        SendData("Close");
    }

}
