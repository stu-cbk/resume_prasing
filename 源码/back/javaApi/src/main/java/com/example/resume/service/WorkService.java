package com.example.resume.service;

import com.example.resume.entity.WorkInformation;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface WorkService {
    List<WorkInformation> showAllData();
    Integer updateOneData(WorkInformation resume);
    Integer insertOneData(WorkInformation resume);
    WorkInformation selectByName(String name);
    WorkInformation selectById(Integer id);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
}
