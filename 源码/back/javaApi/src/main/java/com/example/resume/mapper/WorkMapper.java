package com.example.resume.mapper;

import com.example.resume.entity.WorkInformation;

import java.util.List;

public interface WorkMapper {
    WorkInformation selectByName(String name);
    WorkInformation selectById(Integer id);
    List<WorkInformation> selectAllData();
    Integer addOneData(WorkInformation resume);
    Integer deleteByName(String name);
    Integer deleteById(Integer id);
    Integer updateOneData(WorkInformation resume);
}
