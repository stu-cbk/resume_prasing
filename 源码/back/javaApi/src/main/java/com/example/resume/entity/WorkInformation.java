package com.example.resume.entity;

import lombok.Data;

@Data
public class WorkInformation {
    Integer id;
    String name;
    String targetJob;
    String jobs;
    Integer workExperience;
    String companies;

    Integer engineer;
    Integer finance;
    Integer design;
    Integer manager;
    Integer market;
    Integer hospital;
    Integer edit;
    Integer elseJob;
}
