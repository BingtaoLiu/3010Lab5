package com.example.homeautomation;

import org.json.JSONException;
import org.json.JSONObject;
import android.annotation.SuppressLint;
import android.os.Bundle;
import android.text.format.Formatter;
import android.util.Log;
import android.view.View;
import android.view.ViewDebug;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;
import java.util.concurrent.TimeUnit;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;



public class MainActivity extends AppCompatActivity {

    private ToggleButton toggleButton;
    private Button closeButton;
    private TextView lightSwitch;
    private TextView tempDisplay;
    private TextView humDisplay;
    private TextView co2Display;
    private TextView methaneDisplay;
    public int state_track;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        state_track = 0;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tempDisplay = (TextView)findViewById(R.id.temp);
        humDisplay = (TextView)findViewById(R.id.hum);
        co2Display = (TextView)findViewById(R.id.co2);
        methaneDisplay = (TextView)findViewById(R.id.methane);
        lightSwitch = (TextView)findViewById(R.id.ls) ;

        addListenerOnButtonClick();
        System.out.println(GetDeviceipMobileData());

        Thread Thread2 = null;
        Thread2 = new Thread(new Thread2());
        Thread2.start();
        state_track = 1;
        System.out.println(state_track);




    }

    public void addListenerOnButtonClick(){
        state_track = 2;
        System.out.println(state_track);
        //Getting the ToggleButton layout xml file
        toggleButton=(ToggleButton)findViewById(R.id.onOff);
        closeButton = (Button)findViewById(R.id.closeApp);
        lightSwitch = (TextView)findViewById(R.id.ls) ;
        lightSwitch.setText(" ") ;
        //Performing action on button click

        toggleButton.setOnClickListener(new View.OnClickListener(){


            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View view) {

                // System.out.println(toggleButton.getText())
                state_track = 3;
                System.out.println(state_track);
                if(toggleButton.isChecked() == true){
                    state_track = 4;
                    System.out.println(state_track);
                    lightSwitch.setText("Light Switch ON");new Thread(new Thread3(toggleButton.getText().toString())).start();
                    Log.d("Hi","Hi");
                    //new Thread(new Thread3(toggleButton.getText().toString())).start();

                } else if (toggleButton.isChecked() == false) {
                    state_track = 5;
                    System.out.println(state_track);
                    lightSwitch.setText("Light Switch OFF");
                    // System.out.println("Hiiii");
                    Log.d("Hey","Hey");


                }

            }

        });

        closeButton.setOnClickListener(new View.OnClickListener(){
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View view) {
                state_track = 6;
                System.out.println(state_track);
                System.out.println("Button Working");
                //send Disconnet message to server

            }

        });


    }

    public String GetDeviceipMobileData(){
        try {
            for (java.util.Enumeration<java.net.NetworkInterface> en = java.net.NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                java.net.NetworkInterface networkinterface = en.nextElement();
                for (java.util.Enumeration<java.net.InetAddress> enumIpAddr = networkinterface.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    java.net.InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()) {
                        return inetAddress.getHostAddress().toString();
                    }
                }
            }
        } catch (Exception ex) {
            Log.e("Current IP", ex.toString());
        }
        return null;
    }



    private BufferedReader input;
    class Thread2 implements Runnable {
        @Override
        public void run() {
            Socket socket = null;
            try {
                socket = new Socket("192.168.0.34",8080);
            } catch (IOException e) {
                e.printStackTrace();
            }
            String message;
            try {
                state_track = 7;
                System.out.println(state_track);
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            } catch (IOException e) {
                e.printStackTrace();
            }

            while (true) {

                try {
                    state_track = 80000000;
                    message = null;
                    System.out.println(state_track);
                    System.out.println(input);
                    if((message = input.readLine()) != null && input.ready()){

                        state_track = 90000000;
                        System.out.println(state_track);
                        if (message != null ) {
                            state_track = 898989898;
                            System.out.println(state_track);
                            final String finalMessage = message.toString();
                            state_track = 96969696;
                            System.out.println(state_track);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    // Log.d("MESS","server:");
                                    System.out.println("server: " + finalMessage + "\n");
                                }
                            });
                        }
                        else{
                            System.out.println("No Message Received");
                        }
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    private PrintWriter output;
    class Thread3 implements Runnable {
        private String message;
        Thread3(String message) {
            this.message = message;
        }
        @Override
        public void run() {
            output.write(message);
            output.flush();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Log.d("MESS2","client: ");
                    System.out.println("Client Sent Message");
                    //etMessage.setText("");
                }
            });
        }
    }

}


