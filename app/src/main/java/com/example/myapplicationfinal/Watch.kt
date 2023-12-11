package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class Watch : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_watch)


        val secondActButton1 = findViewById<Button>(R.id.button2)
        secondActButton1.setOnClickListener {
            val Intent = Intent(this, PurchasePage::class.java)
            startActivity(Intent)
            watchcount += 1
        }
        val secondActButton2 = findViewById<Button>(R.id.imageButton1)
        secondActButton2.setOnClickListener {
            val Intent1 = Intent(this, MainActivity2::class.java)
            startActivity(Intent1)
        }
    }
}