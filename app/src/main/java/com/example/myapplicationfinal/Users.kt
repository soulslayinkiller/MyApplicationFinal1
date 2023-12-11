package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class Users : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_users)

        val secondActButton1 = findViewById<Button>(R.id.buttonback)
        secondActButton1.setOnClickListener {
            val Intent = Intent(this, MainActivity::class.java)
            startActivity(Intent)

        }

        val secondActButton2 = findViewById<Button>(R.id.buttonback2)
        secondActButton2.setOnClickListener {
            val Intent1 = Intent(this, Inventory::class.java)
            startActivity(Intent1)
        }
        val secondActButton23 = findViewById<Button>(R.id.buttonback4)
        secondActButton23.setOnClickListener {
            val Intent15 = Intent(this, Logs::class.java)
            startActivity(Intent15)
        }

    }
}
