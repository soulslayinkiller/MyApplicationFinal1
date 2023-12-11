package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView

class Logs : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_logs)

        (findViewById<View>(R.id.textView10) as TextView).text = timenow.toString() + " Was the Time of the Purchase "


        val secondActButton51 = findViewById<Button>(R.id.button)
        secondActButton51.setOnClickListener {
            val Intent31 = Intent(this, MainActivity::class.java)
            startActivity(Intent31)}
    }
}