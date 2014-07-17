common_queries = {
'get_mp_const':"select const_name as const_ward_name, const_name as id from parliament where order by 1;",
'get_mla_const':"select ac_name as const_ward_name, ac_name as id from assembly where order by 1;",
'get_corporator_const':"select const_ward_name,id from tb_electedrep_master and const_ward_type='Ward' and parent='3' and status='active' order by const_ward_name;",

#'get_ai_avg_blore':"select distinct aia.ai_metric as a1, count(distinct aia.sid),aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse where tse.sid=aia.sid and aia.perc_score=100 group by aia.ai_metric,aia.ai_group;",
#'get_ai_count_blore':"select count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse where tse.sid=aia.sid;",
#'get_ang_count_blore':"select count(distinct tse.sid) from tb_school_electedrep tse where heirarchy=2;",

'get_mp_ids':"select distinct '1' as parent, parliament_name as const_ward_name, parliament_name as mp_const_id, 1 as bang_yn from dise_1213_basic_data where assembly_name is not null;",
'get_mla_ids':"select distinct parliament_name as parent, assembly_name as const_ward_name, assembly_name as mla_const_id, 1 as bang_yn from dise_1213_basic_data where assembly_name is not null;",
'get_ward_ids':"select distinct ward.const_ward_name, se.ward_id, se.bang_yn from tb_school_electedrep se,tb_electedrep_master ward where ward.id = se.ward_id;",
'get_schdist':"select distinct '2' as parent, district as district, district as dist_id, 1 as bang_yn from dise_1213_basic_data;",
'get_preschdist':"select distinct upper(district) as district,dist_id, case when dist_id=8877 or dist_id=8773 then 1 else 2 end as bang_yn from vw_school_dise where sid in (select sid from tb_school_electedrep ) and type=2;",
'get_block':"select distinct district as parent, block_name as block, block_name as blck_id, 1 as bang_yn from dise_1213_basic_data;",
'get_cluster':"select distinct block_name as parent, cluster_name as clust, cluster_name as clst_id, 1 as bang_yn from dise_1213_basic_data;",
'get_proj':"select distinct upper(block) as block,blck_id, case when dist_id=8877 or dist_id=8773 then 1 else 2 end as bang_yn from vw_school_dise where sid in (select sid from tb_school_electedrep ) and type=2;",
'get_circle':"select distinct upper(clust) as clust,clst_id, case when dist_id=8877 or dist_id=8773 then 1 else 2 end as bang_yn from vw_school_dise where sid in (select sid from tb_school_electedrep ) and type=2;",
'get_year':"select distinct '3' as parent, id, year from reports_year"
}

mp_queries = {
'get_dise_avg_parent':"select distinct dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and dfa.score=100 and bd.sch_management=1 group by dfa.df_metric,dfa.df_group;",
'get_dise_count_parent':"select count(distinct dfa.dise_code) from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1;",
'get_sch_count_parent':"select count(distinct bd.school_code) from dise{year}basic_data as bd where bd.sch_management=1;",

'mp_gend_sch':"select unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys), sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and parliament_name=$s group by parliament_name;",

#************************'mp_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=$s and heirarchy=1 group by tssc.mt;",
#'mp_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",

'mp_schcount':"select count(school_code) from dise{year}basic_data where sch_management=1 and parliament_name=$s",

'mp_const_details':"select distinct pc.pc_no as elec_comm_code, pc.const_name as const_ward_name , vem.current_elected_rep as current_elected_rep,'MP Constituency' as const_ward_type, ne.neighbours, vem.current_elected_party as current_elected_party from vw_electrep_master as vem, parliament as pc, reports_neighbours as ne where ne.name=const_name and ne.type='mp' and const_name=$s and pc.pc_no=vem.elec_comm_code and const_ward_type like 'MP%';",

'mp_moi_sch':"select distinct moi.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_moi as moi where moi.id=medium_of_instruction and sch_management=1 and parliament_name=$s group by moi.id;",

#'mp_moi_presch':"select distinct tssc.moi as a1, count(distinct tssc.sid) as a2 from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",

'mp_cat_sch':"select distinct sc.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sch_category=sc.id and sch_management=1 and parliament_name=$s group by sc.name;",

'mp_neighbour_sch':"select distinct parliament_name as const_ward_name, count(distinct school_code) from dise{year}basic_data where sch_management=1 and parliament_name in $s group by parliament_name;",

'mp_neighbour_gendsch':"select distinct parliament_name as const_ward_name, unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys),sum(total_girls)]) as sum from dise{year}basic_data where parliament_name in $s and sch_management=1 group by parliament_name;",

'mp_enrol_sch':"select distinct sc.name as a1, sum(total_boys+total_girls)/count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sc.id=sch_category and sch_management=1 and parliament_name=$s group by sc.id;",

'mp_abs_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and parliament_name=$s;",

'mp_fin_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and parliament_name=$s;",

'mp_tlmgrant_sch':"select bd.parliament_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.parliament_name=$s group by bd.parliament_name, vpd.grant_type, vpd.grant_amount;",

'mp_mtncgrant_sch':"select bd.parliament_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct bd.school_code), vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select school_code as dise_id, CASE WHEN tot_clrooms <= CAST (factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data, dise{year}basic_data where criteria='classroom_count') AS mvdf, dise{year}basic_data as bd, reports_tb_paisa_data vpd2 where mvdf.dise_id=bd.school_code and mvdf.operator = vpd2.operator and bd.sch_management=1 and bd.parliament_name=$s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'mp_annualgrant_sch':"select distinct bd.parliament_name as const_ward_name, sc.name as cat, vpd.grant_type, count(distinct school_code), vpd.grant_amount* count(distinct school_code) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd, reports_school_category as sc where sch_management=1 and vpd.criteria='school_cat' and vpd.factor=sc.name and sc.id=bd.sch_category and bd.parliament_name=$s group by bd.parliament_name, sc.name, vpd.grant_type, vpd.grant_amount;",

'mp_neighbor_annual':"select bd.parliament_name as const_ward_name, sc.name as cat, vpd.grant_type, vpd.grant_amount * count(distinct bd.school_code) as total_grant from reports_tb_paisa_data as vpd, dise{year}basic_data as bd, reports_school_category as sc where vpd.criteria='school_cat' and vpd.factor = sc.name and sc.id=bd.sch_category and sch_management=1 and bd.parliament_name in $s group by const_ward_name, cat,vpd.grant_type,vpd.grant_amount order by const_ward_name, cat;",

'mp_neighbor_tlm':"select bd.parliament_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(bd.male_tch + bd.female_tch - bd.noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='teacher_count' and bd.sch_management=1 and bd.parliament_name in $s group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'mp_neighbor_mntnc':"select bd.parliament_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select bd.school_code as dise_id, CASE WHEN bd.tot_clrooms <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='classroom_count') AS mvdf, reports_tb_paisa_data vpd2, dise{year}basic_data as bd where mvdf.operator = vpd2.operator and bd.school_code=mvdf.dise_id and bd.sch_management=1 and bd.parliament_name in $s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'mp_dise_facility':"select distinct dfa.df_metric, count(distinct dfa.dise_code),dfa.df_group from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.sch_management=1 and cast(bd.school_code as text)=dfa.dise_code and bd.parliament_name=$s and dfa.score=100 group by dfa.df_metric,dfa.df_group;",

'mp_dise_count':"select count(school_code) from dise{year}basic_data where sch_management=1 and parliament_name=$s;",


'mp_neighbours_dise':"select distinct bd.parliament_name as const_ward_name, dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.parliament_name in $s and dfa.score=100 group by const_ward_name, dfa.df_metric, dfa.df_group order by const_ward_name,dfa.df_group;",

#'mp_neighbours_anginfra':"select distinct tem.const_ward_name, aia.ai_metric as a1, count(distinct aia.sid), aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.mp_const_id=tem.id and tem.elec_comm_code in $s and aia.perc_score=100 group by tem.const_ward_name, aia.ai_metric,aia.ai_group order by tem.const_ward_name,aia.ai_group;",

#'mp_neighbours_ai_count':"select tem.const_ward_name, count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.mp_const_id=tem.id and tem.elec_comm_code in $s group by tem.const_ward_name;",

'mp_neighbours_df_count':"select bd.parliament_name as const_ward_name, count(distinct dfa.dise_code) from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.parliament_name in $s group by const_ward_name;",

#'mp_sch_assess_class':"select vra.class as a1, vra.grade, sum(vra.stucount) as count from vw_reading_2011_agg vra, tb_school_electedrep tse where tse.sid=vra.sid and tse.mp_const_id=$s and vra.acyear='2011-2012' and vra.grade not in ('null','',' ') and vra.class is not null group by vra.class, vra.grade;",

}

mla_queries = {

'get_dise_avg_parent':"select distinct dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and dfa.score=100 and bd.sch_management=1 group by dfa.df_metric,dfa.df_group;",
'get_dise_count_parent':"select count(distinct dfa.dise_code) from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1;",
'get_sch_count_parent':"select count(distinct bd.school_code) from dise{year}basic_data as bd where bd.sch_management=1;",

'mla_gend_sch':"select unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys), sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and assembly_name=$s group by assembly_name;",

#************************'mla_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=$s and heirarchy=1 group by tssc.mt;",
#'mla_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",

'mla_schcount':"select count(school_code) from dise{year}basic_data where sch_management=1 and assembly_name=$s",

'mla_const_details':"select distinct pc.ac_no as elec_comm_code, pc.ac_name as const_ward_name , vem.current_elected_rep as current_elected_rep,'MLA Constituency' as const_ward_type, ne.neighbours, vem.current_elected_party as current_elected_party from vw_electrep_master as vem, assembly as pc, reports_neighbours as ne where ne.name=ac_name and ne.type='mla' and ac_name=$s and pc.ac_no=vem.elec_comm_code and const_ward_type like 'MLA%';",

'mla_moi_sch':"select distinct moi.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_moi as moi where moi.id=medium_of_instruction and sch_management=1 and assembly_name=$s group by moi.id;",

#'mla_moi_presch':"select distinct tssc.moi as a1, count(distinct tssc.sid) as a2 from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",

'mla_cat_sch':"select distinct sc.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sch_category=sc.id and sch_management=1 and assembly_name=$s group by sc.name;",

'mla_neighbour_sch':"select distinct assembly_name as const_ward_name, count(distinct school_code) from dise{year}basic_data where assembly_name in $s and sch_management=1 group by assembly_name;",

'mla_neighbour_gendsch':"select distinct assembly_name as const_ward_name, unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys),sum(total_girls)]) as sum from dise{year}basic_data where assembly_name in $s and sch_management=1 group by assembly_name;",

'mla_enrol_sch':"select distinct sc.name as a1, sum(total_boys+total_girls)/count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sc.id=sch_category and sch_management=1 and assembly_name=$s group by sc.id;",

'mla_abs_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and assembly_name=$s;",

'mla_fin_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and assembly_name=$s;",

'mla_tlmgrant_sch':"select bd.assembly_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.assembly_name=$s group by bd.assembly_name, vpd.grant_type, vpd.grant_amount;",

'mla_mtncgrant_sch':"select bd.assembly_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct bd.school_code), vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select school_code as dise_id, CASE WHEN tot_clrooms <= CAST (factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data, dise{year}basic_data where criteria='classroom_count') AS mvdf, dise{year}basic_data as bd, reports_tb_paisa_data vpd2 where mvdf.dise_id=bd.school_code and mvdf.operator = vpd2.operator and bd.sch_management=1 and bd.assembly_name=$s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'mla_annualgrant_sch':"select distinct bd.assembly_name as const_ward_name, sc.name as cat, vpd.grant_type, count(distinct school_code), vpd.grant_amount* count(distinct school_code) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd, reports_school_category as sc where sch_management=1 and vpd.criteria='school_cat' and vpd.factor=sc.name and sc.id=bd.sch_category and bd.assembly_name=$s group by bd.assembly_name, sc.name, vpd.grant_type, vpd.grant_amount;",

'mla_neighbor_annual':"select bd.assembly_name as const_ward_name, sc.name as cat, vpd.grant_type, vpd.grant_amount * count(distinct bd.school_code) as total_grant from reports_tb_paisa_data as vpd, dise{year}basic_data as bd, reports_school_category as sc where vpd.criteria='school_cat' and vpd.factor = sc.name and sc.id=bd.sch_category and sch_management=1 and bd.assembly_name in $s group by const_ward_name, cat,vpd.grant_type,vpd.grant_amount order by const_ward_name, cat;",

'mla_neighbor_tlm':"select bd.assembly_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(bd.male_tch + bd.female_tch - bd.noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='teacher_count' and bd.sch_management=1 and bd.assembly_name in $s group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'mla_neighbor_mntnc':"select bd.assembly_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select bd.school_code as dise_id, CASE WHEN bd.tot_clrooms <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='classroom_count') AS mvdf, reports_tb_paisa_data vpd2, dise{year}basic_data as bd where mvdf.operator = vpd2.operator and bd.school_code=mvdf.dise_id and bd.sch_management=1 and bd.assembly_name in $s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'mla_dise_facility':"select distinct dfa.df_metric, count(distinct dfa.dise_code),dfa.df_group from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.sch_management=1 and cast(bd.school_code as text)=dfa.dise_code and bd.assembly_name=$s and dfa.score=100 group by dfa.df_metric,dfa.df_group;",

'mla_dise_count':"select count(school_code) from dise{year}basic_data where sch_management=1 and assembly_name=$s;",


'mla_neighbours_dise':"select distinct bd.assembly_name as const_ward_name, dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.assembly_name in $s and dfa.score=100 group by const_ward_name, dfa.df_metric, dfa.df_group order by const_ward_name,dfa.df_group;",

#'mla_neighbours_anginfra':"select distinct tem.const_ward_name, aia.ai_metric as a1, count(distinct aia.sid), aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.mla_const_id=tem.id and tem.elec_comm_code in $s and aia.perc_score=100 group by tem.const_ward_name, aia.ai_metric,aia.ai_group order by tem.const_ward_name,aia.ai_group;",

#'mla_neighbours_ai_count':"select tem.const_ward_name, count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.mla_const_id=tem.id and tem.elec_comm_code in $s group by tem.const_ward_name;",

'mla_neighbours_df_count':"select bd.assembly_name as const_ward_name, count(distinct dfa.dise_code) from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.assembly_name in $s group by const_ward_name;",

#'mla_sch_assess_class':"select vra.class as a1, vra.grade, sum(vra.stucount) as count from vw_reading_2011_agg vra, tb_school_electedrep tse where tse.sid=vra.sid and tse.mla_const_id=$s and vra.acyear='2011-2012' and vra.grade not in ('null','',' ') and vra.class is not null group by vra.class, vra.grade;",

}

"""cluster_queries = {
'cluster_mdm_agg':"select mon,wk,sum(indent) as indent,sum(attend) as attend, sd.clust as name from vw_school_dise sd, vw_mdm_agg mdm where mdm.id=sd.sid and sd.clst_id=$s group by mon,wk,clust order by mon,wk;",
'cluster_klp_enrol':"select sum(case when sex='Boy' then tssc.numstu end) as num_boys,sum(case when sex='Girl' then tssc.numstu end) as num_girls from vw_school_dise sd, tb_school_stu_counts tssc where tssc.sid=sd.sid and sd.clst_id=$s and sd.sid in (select distinct id from vw_mdm_agg);",
'cluster_dise_enrol':"select sum(boys_count) as num_boys,sum(girls_count) as num_girls from vw_school_dise sd,vw_dise_info vdi where vdi.dise_code=sd.dise_code and sd.clst_id=$s and sd.sid in (select distinct id from vw_mdm_agg);",
'cluster_sch_count':"select count(distinct sd.sid) as a1,count(distinct mdm.id) as a2 from vw_school_dise sd left join vw_mdm_agg mdm on mdm.id=sd.sid where sd.clst_id=$s;"
} 

block_queries = {
'block_mdm_agg':"select mon,wk,sum(indent) as indent,sum(attend) as attend, sd.block as name from vw_school_dise sd, vw_mdm_agg mdm where mdm.id=sd.sid and sd.blck_id=$s group by mon,wk,block order by mon,wk;",
'block_klp_enrol':"select sum(case when sex='Boy' then tssc.numstu end) as num_boys,sum(case when sex='Girl' then tssc.numstu end) as num_girls from vw_school_dise sd, tb_school_stu_counts tssc where tssc.sid=sd.sid and sd.blck_id=$s and sd.sid in (select distinct id from vw_mdm_agg);",
'block_dise_enrol':"select sum(boys_count) as num_boys,sum(girls_count) as num_girls from vw_school_dise sd,vw_dise_info vdi where vdi.dise_code=sd.dise_code and sd.blck_id=$s and sd.sid in (select distinct id from vw_mdm_agg);",
'block_sch_count':"select count(distinct sd.sid) as a1,count(distinct mdm.id) as a2 from vw_school_dise sd left join vw_mdm_agg mdm on mdm.id=sd.sid where sd.blck_id=$s;"
}"""

cluster_queries = {
'get_dise_avg_parent':"select distinct dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and dfa.score=100 and bd.sch_management=1 and bd.block_name=(select distinct block_name from dise{year}basic_data where cluster_name=$s) group by dfa.df_metric,dfa.df_group;",
'get_dise_count_parent':"select count(distinct dfa.dise_code) from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.block_name=(select distinct block_name from dise{year}basic_data where cluster_name='ACHAVE');",
'get_sch_count_parent':"select count(distinct bd.school_code) from dise{year}basic_data as bd where bd.sch_management=1 and bd.block_name=(select distinct block_name from dise{year}basic_data where cluster_name=$s);",

'cluster_gend_sch':"select unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys), sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and cluster_name=$s group by cluster_name;",

#************************'cluster_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.cluster_const_id=$s and heirarchy=1 group by tssc.mt;",
#'cluster_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.cluster_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",

'cluster_schcount':"select count(school_code) from dise{year}basic_data where sch_management=1 and cluster_name=$s;",

'cluster_const_details':"select distinct 1 as elec_comm_code, cluster_name as const_ward_name , district as current_elected_rep,'cluster_name' as const_ward_type, array_to_string(array(select distinct cluster_name from dise{year}basic_data as blck where blck.block_name=clst.block_name),'|') as neighbours, block_name as current_elected_party from dise{year}basic_data as clst where sch_management=1 and clst.cluster_name=$s limit 1;",

'cluster_moi_sch':"select distinct moi.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_moi as moi where moi.id=medium_of_instruction and sch_management=1 and cluster_name=$s group by moi.id;",

#'cluster_moi_presch':"select distinct tssc.moi as a1, count(distinct tssc.sid) as a2 from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.cluster_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",

'cluster_cat_sch':"select distinct sc.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sch_category=sc.id and sch_management=1 and cluster_name=$s group by sc.name;",

'cluster_neighbour_sch':"select distinct cluster_name as const_ward_name, count(distinct school_code) from dise{year}basic_data where sch_management = 1 and cluster_name in $s group by cluster_name;",

'cluster_neighbour_gendsch':"select distinct cluster_name as const_ward_name, unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys),sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and cluster_name in $s and sch_management=1 group by cluster_name;",

'cluster_enrol_sch':"select distinct sc.name as a1, sum(total_boys+total_girls)/count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sc.id=sch_category and sch_management=1 and cluster_name=$s group by sc.id;",

'cluster_abs_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and cluster_name=$s;",

'cluster_fin_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and cluster_name=$s;",

'cluster_tlmgrant_sch':"select bd.cluster_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.cluster_name=$s group by bd.cluster_name, vpd.grant_type, vpd.grant_amount;",

'cluster_mtncgrant_sch':"select bd.cluster_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct bd.school_code), vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select school_code as dise_id, CASE WHEN tot_clrooms <= CAST (factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data, dise{year}basic_data where criteria='classroom_count') AS mvdf, dise{year}basic_data as bd, reports_tb_paisa_data vpd2 where mvdf.dise_id=bd.school_code and mvdf.operator = vpd2.operator and bd.sch_management=1 and bd.cluster_name=$s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'cluster_annualgrant_sch':"select distinct bd.cluster_name as const_ward_name, sc.name as cat, vpd.grant_type, count(distinct school_code), vpd.grant_amount* count(distinct school_code) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd, reports_school_category as sc where sch_management=1 and vpd.criteria='school_cat' and vpd.factor=sc.name and sc.id=bd.sch_category and bd.cluster_name=$s group by const_ward_name, sc.name, vpd.grant_type, vpd.grant_amount;",

'cluster_neighbor_annual':"select bd.cluster_name as const_ward_name, sc.name as cat, vpd.grant_type, vpd.grant_amount * count(distinct bd.school_code) as total_grant from reports_tb_paisa_data as vpd, dise{year}basic_data as bd, reports_school_category as sc where vpd.criteria='school_cat' and vpd.factor = sc.name and sc.id=bd.sch_category and sch_management=1 and bd.cluster_name in $s group by const_ward_name, cat,vpd.grant_type,vpd.grant_amount order by const_ward_name, cat;",

'cluster_neighbor_tlm':"select bd.cluster_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(bd.male_tch + bd.female_tch - bd.noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='teacher_count' and bd.sch_management=1 and bd.cluster_name in $s group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'cluster_neighbor_mntnc':"select bd.cluster_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select bd.school_code as dise_id, CASE WHEN bd.tot_clrooms <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='classroom_count') AS mvdf, reports_tb_paisa_data vpd2, dise{year}basic_data as bd where mvdf.operator = vpd2.operator and bd.school_code=mvdf.dise_id and bd.sch_management=1 and bd.cluster_name in $s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'cluster_dise_facility':"select distinct dfa.df_metric, count(distinct dfa.dise_code),dfa.df_group from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.sch_management=1 and cast(bd.school_code as text)=dfa.dise_code and bd.cluster_name=$s and dfa.score=100 group by dfa.df_metric,dfa.df_group;",

'cluster_dise_count':"select count(school_code) from dise{year}basic_data where sch_management=1 and cluster_name=$s;",


'cluster_neighbours_dise':"select distinct bd.cluster_name as const_ward_name, dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.cluster_name in $s and dfa.score=100 group by const_ward_name, dfa.df_metric, dfa.df_group order by const_ward_name,dfa.df_group;",

#'cluster_neighbours_anginfra':"select distinct tem.const_ward_name, aia.ai_metric as a1, count(distinct aia.sid), aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.cluster_const_id=tem.id and tem.elec_comm_code in $s and aia.perc_score=100 group by tem.const_ward_name, aia.ai_metric,aia.ai_group order by tem.const_ward_name,aia.ai_group;",

#'cluster_neighbours_ai_count':"select tem.const_ward_name, count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.cluster_const_id=tem.id and tem.elec_comm_code in $s group by tem.const_ward_name;",

'cluster_neighbours_df_count':"select bd.cluster_name as const_ward_name, count(distinct dfa.dise_code) from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.cluster_name in $s group by const_ward_name;",

#'cluster_sch_assess_class':"select vra.class as a1, vra.grade, sum(vra.stucount) as count from vw_reading_2011_agg vra, tb_school_electedrep tse where tse.sid=vra.sid and tse.cluster_const_id=$s and vra.acyear='2011-2012' and vra.grade not in ('null','',' ') and vra.class is not null group by vra.class, vra.grade;",

}

block_queries = {
'get_dise_avg_parent':"select distinct dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and dfa.score=100 and bd.sch_management=1 and bd.district=(select distinct district from dise{year}basic_data where block_name=$s) group by dfa.df_metric,dfa.df_group;",
'get_dise_count_parent':"select count(distinct dfa.dise_code) from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.district=(select distinct district from dise{year}basic_data where block_name=$s);",
'get_sch_count_parent':"select count(distinct bd.school_code) from dise{year}basic_data as bd where bd.sch_management=1 and bd.district=(select distinct district from dise{year}basic_data where block_name=$s);",

'block_gend_sch':"select unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys), sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and block_name=$s group by block_name;",

#************************'block_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.block_const_id=$s and heirarchy=1 group by tssc.mt;",
#'block_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.block_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",

'block_schcount':"select count(school_code) from dise{year}basic_data where sch_management=1 and block_name=$s;",

'block_const_details':"select distinct 1 as elec_comm_code, block_name as const_ward_name , district as current_elected_rep,'block_name' as const_ward_type, array_to_string(array(select distinct block_name from dise{year}basic_data as dist where dist.district=blck.district),'|') as neighbours, block_name as current_elected_party from dise{year}basic_data as blck where sch_management=1 and block_name=$s;",

'block_moi_sch':"select distinct moi.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_moi as moi where moi.id=medium_of_instruction and sch_management=1 and block_name=$s group by moi.id;",

#'block_moi_presch':"select distinct tssc.moi as a1, count(distinct tssc.sid) as a2 from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.block_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",

'block_cat_sch':"select distinct sc.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sch_category=sc.id and sch_management=1 and block_name=$s group by sc.name;",

'block_neighbour_sch':"select distinct block_name as const_ward_name, count(distinct school_code) from dise{year}basic_data where sch_management = 1 and block_name in $s group by block_name;",

'block_neighbour_gendsch':"select distinct block_name as const_ward_name, unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys),sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and block_name in $s and sch_management=1 group by block_name;",

'block_enrol_sch':"select distinct sc.name as a1, sum(total_boys+total_girls)/count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sc.id=sch_category and sch_management=1 and block_name=$s group by sc.id;",

'block_abs_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and block_name=$s;",

'block_fin_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and block_name=$s;",

'block_tlmgrant_sch':"select bd.block_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.block_name=$s group by bd.block_name, vpd.grant_type, vpd.grant_amount;",

'block_mtncgrant_sch':"select bd.block_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct bd.school_code), vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select school_code as dise_id, CASE WHEN tot_clrooms <= CAST (factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data, dise{year}basic_data where criteria='classroom_count') AS mvdf, dise{year}basic_data as bd, reports_tb_paisa_data vpd2 where mvdf.dise_id=bd.school_code and mvdf.operator = vpd2.operator and bd.sch_management=1 and bd.block_name=$s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'block_annualgrant_sch':"select distinct bd.block_name as const_ward_name, sc.name as cat, vpd.grant_type, count(distinct school_code), vpd.grant_amount* count(distinct school_code) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd, reports_school_category as sc where sch_management=1 and vpd.criteria='school_cat' and vpd.factor=sc.name and sc.id=bd.sch_category and bd.block_name=$s group by const_ward_name, sc.name, vpd.grant_type, vpd.grant_amount;",

'block_neighbor_annual':"select bd.block_name as const_ward_name, sc.name as cat, vpd.grant_type, vpd.grant_amount * count(distinct bd.school_code) as total_grant from reports_tb_paisa_data as vpd, dise{year}basic_data as bd, reports_school_category as sc where vpd.criteria='school_cat' and vpd.factor = sc.name and sc.id=bd.sch_category and sch_management=1 and bd.block_name in $s group by const_ward_name, cat,vpd.grant_type,vpd.grant_amount order by const_ward_name, cat;",

'block_neighbor_tlm':"select bd.block_name as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(bd.male_tch + bd.female_tch - bd.noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='teacher_count' and bd.sch_management=1 and bd.block_name in $s group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'block_neighbor_mntnc':"select bd.block_name as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select bd.school_code as dise_id, CASE WHEN bd.tot_clrooms <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='classroom_count') AS mvdf, reports_tb_paisa_data vpd2, dise{year}basic_data as bd where mvdf.operator = vpd2.operator and bd.school_code=mvdf.dise_id and bd.sch_management=1 and bd.block_name in $s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'block_dise_facility':"select distinct dfa.df_metric, count(distinct dfa.dise_code),dfa.df_group from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.sch_management=1 and cast(bd.school_code as text)=dfa.dise_code and bd.block_name=$s and dfa.score=100 group by dfa.df_metric,dfa.df_group;",

'block_dise_count':"select count(school_code) from dise{year}basic_data where sch_management=1 and block_name=$s;",


'block_neighbours_dise':"select distinct bd.block_name as const_ward_name, dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.block_name in $s and dfa.score=100 group by const_ward_name, dfa.df_metric, dfa.df_group order by const_ward_name,dfa.df_group;",

#'block_neighbours_anginfra':"select distinct tem.const_ward_name, aia.ai_metric as a1, count(distinct aia.sid), aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.block_const_id=tem.id and tem.elec_comm_code in $s and aia.perc_score=100 group by tem.const_ward_name, aia.ai_metric,aia.ai_group order by tem.const_ward_name,aia.ai_group;",

#'block_neighbours_ai_count':"select tem.const_ward_name, count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.block_const_id=tem.id and tem.elec_comm_code in $s group by tem.const_ward_name;",

'block_neighbours_df_count':"select bd.block_name as const_ward_name, count(distinct dfa.dise_code) from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.block_name in $s group by const_ward_name;",

#'block_sch_assess_class':"select vra.class as a1, vra.grade, sum(vra.stucount) as count from vw_reading_2011_agg vra, tb_school_electedrep tse where tse.sid=vra.sid and tse.block_const_id=$s and vra.acyear='2011-2012' and vra.grade not in ('null','',' ') and vra.class is not null group by vra.class, vra.grade;",

}


district_queries = {

'get_dise_avg_parent':"select distinct dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and dfa.score=100 and bd.sch_management=1 group by dfa.df_metric,dfa.df_group;",
'get_dise_count_parent':"select count(distinct dfa.dise_code) from reports{year}basic_data_agg as dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1;",
'get_sch_count_parent':"select count(distinct bd.school_code) from dise{year}basic_data as bd where bd.sch_management=1;",

'district_gend_sch':"select unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys), sum(total_girls)]) as sum from dise{year}basic_data where sch_management=1 and district=$s group by district;",

#************************'district_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.district_const_id=$s and heirarchy=1 group by tssc.mt;",
#'district_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.district_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",

'district_schcount':"select count(school_code) from dise{year}basic_data where sch_management=1 and district=$s;",

#'district_const_details':"select distinct 1 as elec_comm_code, district as const_ward_name , 'hello' as current_elected_rep,'district' as const_ward_type, array_to_string(array(select distinct district from dise{year}basic_data as dist),'|') as neighbours, 'world' as current_elected_party from dise{year}basic_data as blck where sch_management=1 and district=$s",

'district_const_details':"select distinct 1 as elec_comm_code, district as const_ward_name , 'hello' as current_elected_rep,'district' as const_ward_type, ne.neighbours, 'world' as current_elected_party from dise{year}basic_data as bd, reports_neighbours as ne where sch_management=1 and ne.name=bd.district and ne.type='district' and district=$s",

'district_moi_sch':"select distinct moi.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_moi as moi where moi.id=medium_of_instruction and sch_management=1 and district=$s group by moi.id;",

#'district_moi_presch':"select distinct tssc.moi as a1, count(distinct tssc.sid) as a2 from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.district_const_id=$s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",

'district_cat_sch':"select distinct sc.name as a1, count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sch_category=sc.id and sch_management=1 and district=$s group by sc.name;",

'district_neighbour_sch':"select distinct district as const_ward_name, count(distinct school_code) from dise{year}basic_data where sch_management=1 and district in $s group by district;",

'district_neighbour_gendsch':"select distinct district as const_ward_name, unnest(ARRAY['Boy','Girl']) as sex, unnest(ARRAY[sum(total_boys),sum(total_girls)]) as sum from dise{year}basic_data where district in $s and sch_management=1 group by district;",

'district_enrol_sch':"select distinct sc.name as a1, sum(total_boys+total_girls)/count(distinct school_code) as a2 from dise{year}basic_data, reports_school_category as sc where sc.id=sch_category and sch_management=1 and district=$s group by sc.id;",

'district_abs_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and district=$s;",

'district_fin_schcount':"select count(distinct school_code) from dise{year}basic_data where sch_management=1 and district=$s;",

'district_tlmgrant_sch':"select bd.district as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.district='UDUPI' group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'district_grant_sch':"select bd.district as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(male_tch + female_tch - noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where sch_management=1 and vpd.criteria='teacher_count' and bd.district=$s group by bd.district, vpd.grant_type, vpd.grant_amount;",

'district_mtncgrant_sch':"select bd.district as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct bd.school_code), vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select school_code as dise_id, CASE WHEN tot_clrooms <= CAST (factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data, dise{year}basic_data where criteria='classroom_count') AS mvdf, dise{year}basic_data as bd, reports_tb_paisa_data vpd2 where mvdf.dise_id=bd.school_code and mvdf.operator = vpd2.operator and bd.sch_management=1 and bd.district=$s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'district_annualgrant_sch':"select distinct bd.district as const_ward_name, sc.name as cat, vpd.grant_type, count(distinct school_code), vpd.grant_amount* count(distinct school_code) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd, reports_school_category as sc where sch_management=1 and vpd.criteria='school_cat' and vpd.factor=sc.name and sc.id=bd.sch_category and bd.district=$s group by const_ward_name, sc.name, vpd.grant_type, vpd.grant_amount;",

'district_neighbor_annual':"select bd.district as const_ward_name, sc.name as cat, vpd.grant_type, vpd.grant_amount * count(distinct bd.school_code) as total_grant from reports_tb_paisa_data as vpd, dise{year}basic_data as bd, reports_school_category as sc where vpd.criteria='school_cat' and vpd.factor = sc.name and sc.id=bd.sch_category and sch_management=1 and bd.district in $s group by const_ward_name, cat,vpd.grant_type,vpd.grant_amount order by const_ward_name, cat;",

'district_neighbor_tlm':"select bd.district as const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(bd.male_tch + bd.female_tch - bd.noresp_tch) as total_grant from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='teacher_count' and bd.sch_management=1 and bd.district in $s group by const_ward_name, vpd.grant_type, vpd.grant_amount;",

'district_neighbor_mntnc':"select bd.district as const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct bd.school_code) as total_grant from (select bd.school_code as dise_id, CASE WHEN bd.tot_clrooms <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from reports_tb_paisa_data vpd, dise{year}basic_data as bd where vpd.criteria='classroom_count') AS mvdf, reports_tb_paisa_data vpd2, dise{year}basic_data as bd where mvdf.operator = vpd2.operator and bd.school_code=mvdf.dise_id and bd.sch_management=1 and bd.district in $s group by const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by const_ward_name;",

'district_dise_facility':"select distinct dfa.df_metric, count(distinct dfa.dise_code),dfa.df_group from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.sch_management=1 and cast(bd.school_code as text)=dfa.dise_code and bd.district=$s and dfa.score=100 group by dfa.df_metric,dfa.df_group;",

'district_dise_count':"select count(school_code) from dise{year}basic_data where sch_management=1 and district=$s;",


'district_neighbours_dise':"select distinct bd.district as const_ward_name, dfa.df_metric as a1, count(distinct dfa.dise_code),dfa.df_group as a2 from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.district in $s and dfa.score=100 group by const_ward_name, dfa.df_metric, dfa.df_group order by const_ward_name,dfa.df_group;",

#'district_neighbours_anginfra':"select distinct tem.const_ward_name, aia.ai_metric as a1, count(distinct aia.sid), aia.ai_group as a2 from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.district_const_id=tem.id and tem.elec_comm_code in $s and aia.perc_score=100 group by tem.const_ward_name, aia.ai_metric,aia.ai_group order by tem.const_ward_name,aia.ai_group;",

#'district_neighbours_ai_count':"select tem.const_ward_name, count(distinct aia.sid) from vw_ang_infra_agg aia, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=aia.sid and tse.district_const_id=tem.id and tem.elec_comm_code in $s group by tem.const_ward_name;",

'district_neighbours_df_count':"select bd.district as const_ward_name, count(distinct dfa.dise_code) from reports{year}basic_data_agg dfa, dise{year}basic_data as bd where bd.school_code::text=dfa.dise_code and bd.sch_management=1 and bd.district in $s group by const_ward_name;",

#'district_sch_assess_class':"select vra.class as a1, vra.grade, sum(vra.stucount) as count from vw_reading_2011_agg vra, tb_school_electedrep tse where tse.sid=vra.sid and tse.district_const_id=$s and vra.acyear='2011-2012' and vra.grade not in ('null','',' ') and vra.class is not null group by vra.class, vra.grade;",

}

#dicts={'mp':mp_queries,'mla':mla_queries,'district':district_queries,'block':block_queries,'cluster':cluster_queries}

def getDictionary(constype = 'common'):
  if constype == 'mp':
    return replace_year(mp_queries)
  elif constype == 'mla':
    return replace_year(mla_queries)
  elif constype == 'corporator':
    return corporator_queries
  elif constype == 'cluster':
    return replace_year(cluster_queries)
  elif constype == 'block':
    return replace_year(block_queries)
  elif constype == 'district':
    return replace_year(district_queries)
  elif constype == 'block':
    return replace_year(block_queries)
  elif constype == 'cluster':
    return replace_year(cluster_queries)
  else:
    return common_queries

year=''

def replace_year(queries):
    dicts={}
    for key in queries:
        dicts[key]=queries[key].replace('{year}','_'+year+'_')
    return dicts

def select_year(value = '1213'):
    global year
    year=value
