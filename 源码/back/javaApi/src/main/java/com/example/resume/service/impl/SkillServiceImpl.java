package com.example.resume.service.impl;

import com.example.resume.entity.SkillInformation;
import com.example.resume.mapper.SkillMapper;
import com.example.resume.service.SkillService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
public class SkillServiceImpl implements SkillService {
    @Resource
    private SkillMapper resumeMapper;

    @Override
    public List<SkillInformation> showAllData(){return resumeMapper.selectAllData();}

    @Override
    public Integer updateOneData(SkillInformation resume){return resumeMapper.updateOneData(resume);}

    @Override
    public Integer insertOneData(SkillInformation resume){return resumeMapper.addOneData(resume);}

    @Override
    public SkillInformation selectByName(String name){return resumeMapper.selectByName(name);}

    @Override
    public SkillInformation selectById(Integer id){return resumeMapper.selectById(id);}

    @Override
    public Integer deleteByName(String name){return resumeMapper.deleteByName(name);}

    @Override
    public Integer deleteById(Integer id){return resumeMapper.deleteById(id);}
}
