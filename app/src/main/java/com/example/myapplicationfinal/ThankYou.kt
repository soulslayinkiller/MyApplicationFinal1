package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class ThankYou : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_thank_you)

        val secondActButton2 = findViewById<Button>(R.id.button)
        secondActButton2.setOnClickListener {
            val Intent1 = Intent(this, MainActivity::class.java)
            startActivity(Intent1)
        }
    }
}