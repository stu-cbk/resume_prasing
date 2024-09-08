package com.example.resume.service.impl;

import com.example.resume.entity.WorkInformation;
import com.example.resume.mapper.WorkMapper;
import com.example.resume.service.WorkService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class WorkServiceImpl implements WorkService {
    @Resource
    private WorkMapper resumeMapper;

    @Override
    public List<WorkInformation> showAllData(){return resumeMapper.selectAllData();}

    @Override
    public Integer updateOneData(WorkInformation resume){return resumeMapper.updateOneData(resume);}

    @Override
    public Integer insertOneData(WorkInformation resume){return resumeMapper.addOneData(resume);}

    @Override
    public WorkInformation selectByName(String name){return resumeMapper.selectByName(name);}

    @Override
    public WorkInformation selectById(Integer id){return resumeMapper.selectById(id);}

    @Override
    public Integer deleteByName(String name){return resumeMapper.deleteByName(name);}

    @Override
    public Integer deleteById(Integer id){return resumeMapper.deleteById(id);}
}
