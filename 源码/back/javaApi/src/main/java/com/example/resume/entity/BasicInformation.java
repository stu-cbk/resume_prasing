package com.example.resume.entity;

import lombok.Data;

@Data
public class BasicInformation {
    Integer id;
    String name;
    Integer age;
    String gender;

    String origin;
    String identity;
    String phone;
    String email;
    String text;
}
