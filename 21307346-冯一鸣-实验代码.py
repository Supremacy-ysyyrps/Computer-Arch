import copy
# 指令的操作类型
OP = ["ld","mul","div","add","sub"]
# 指令状态表
INS_STAT = []
# 功能部件
FU = ["int","mul1","mul2","div","add"]
# 功能部件状态表，num是占据该功能部件的指令在指令序列中的编号
STAT = ["busy","op","fi","fj","fk","qj","qk","rj","rk","num"]
FU_STAT = {fu:{s:"" for s in STAT} for fu in FU}
# 结果寄存器状态表
REGS_STAT = {"f0":"","f1":"","f2":"","f3":"","f4":"","f5":"","f6":"","f7":"","f8":"","f9":"","f10":""}
# 上一周期执行完RO的指令，用于本周期执行EX
flag_ex = {fu:False for fu in FU}
# 上一周期执行完EX的指令，用于本周期执行WR
flag_wr = {fu:False for fu in FU}


def show():
	print("Instruction status table:")
	print("INS\t","IS","RO","EX","WR",sep="\t")
	for i in INS_STAT:
		for i_s in i.values():
			print(i_s,end="\t")
		print("")
	print("\nFunctional unit status:")
	print("FU","busy","op","fi","fj","fk","qj","qk","rj","rk","num",sep="\t")
	for fu in FU:
		print(fu,end='\t')
		for s in FU_STAT[fu].values():
			print(s,end='\t')
		print("")
	print("\nRegister result status:")
	for reg_name in REGS_STAT.keys():
		print(reg_name,end="\t")
	print("")
	for reg_stat in REGS_STAT.values():
		print(reg_stat,end="\t")
	print("")


# 输入指令
print("Only support instructions: ", OP)
I = input("Please input instructions in the form :\n'op rd rs rt'\nor\n'op rt imm rs'\n")
while I:
	INS_STAT.append({"INS":I,"IS":"","RO":"","EX":"","WR":""})
	I = input()
input("Press any key to start execution: ")


# 开始执行
i = 0 # 当前位于指令队列队首的指令序号
c = 0 # 当前时钟周期序号
while i < len(INS_STAT):
	# 显示状态
	print("Cycle ",c)
	show()
	c += 1
	# 深拷贝FU_STAT，因为状态是每个时钟周期更新一次
	FU_STAT_ = copy.deepcopy(FU_STAT)

	# IS
	flag_is = 0 # 本周期是否可以发射指令
	INS = INS_STAT[i]["INS"].split() # 取出当前位于指令队列队首的指令
	if(INS[0] == "ld"): # 判断指令类型
		# 根据指令类型检查所需功能单元是否可用（排除结构冒险）
		# 检查是否有其他指令需要写入同一目的寄存器（排除WAW冒险）
		# 若没有上述两种冒险，则发射指令并更新功能单元状态表和寄存器状态表
		if(not FU_STAT["int"]["busy"] and not REGS_STAT[INS[1]]):
			FU_STAT_["int"]["busy"] = True
			FU_STAT_["int"]["op"] = "ld"
			FU_STAT_["int"]["fi"] = INS[1]
			FU_STAT_["int"]["fj"] = "null"
			FU_STAT_["int"]["fk"] = INS[3]
			FU_STAT_["int"]["qj"] = ""
			FU_STAT_["int"]["qk"] = REGS_STAT[INS[3]]
			FU_STAT_["int"]["rj"] = not FU_STAT_["int"]["qj"]
			FU_STAT_["int"]["rk"] = not FU_STAT_["int"]["qk"]
			FU_STAT_["int"]["num"] = i
			REGS_STAT[INS[1]] = 'int'
			flag_is = 1
	elif(INS[0] == 'mul'):
		m = ''
		if(not FU_STAT["mul1"]["busy"]):
			m = "mul1"
		elif(not FU_STAT["mul2"]["busy"]):
			m = "mul2"
		if(m and not REGS_STAT[INS[1]]):
			FU_STAT_[m]["busy"] = True
			FU_STAT_[m]["op"] = "mul"
			FU_STAT_[m]["fi"] = INS[1]
			FU_STAT_[m]["fj"] = INS[2]
			FU_STAT_[m]["fk"] = INS[3]
			FU_STAT_[m]["qj"] = REGS_STAT[INS[2]]
			FU_STAT_[m]["qk"] = REGS_STAT[INS[3]]
			FU_STAT_[m]["rj"] = not FU_STAT_[m]["qj"]
			FU_STAT_[m]["rk"] = not FU_STAT_[m]["qk"]
			FU_STAT_[m]["num"] = i
			REGS_STAT[INS[1]] = m
			flag_is = 1
	elif(INS[0] == "div"):
		if(not FU_STAT["div"]["busy"] and not REGS_STAT[INS[1]]):
			FU_STAT_["div"]["busy"] = True
			FU_STAT_["div"]["op"] = "div"
			FU_STAT_["div"]["fi"] = INS[1]
			FU_STAT_["div"]["fj"] = INS[2]
			FU_STAT_["div"]["fk"] = INS[3]
			FU_STAT_["div"]["qj"] = REGS_STAT[INS[2]]
			FU_STAT_["div"]["qk"] = REGS_STAT[INS[3]]
			FU_STAT_["div"]["rj"] = not FU_STAT_["div"]["qj"]
			FU_STAT_["div"]["rk"] = not FU_STAT_["div"]["qk"]
			FU_STAT_["div"]["num"] = i
			REGS_STAT[INS[1]] = "div"
			flag_is = 1
	elif(INS[0] == "add"):
		if(not FU_STAT["add"]["busy"] and not REGS_STAT[INS[1]]):
			FU_STAT_["add"]["busy"] = True
			FU_STAT_["add"]["op"] = "mul"
			FU_STAT_["add"]["fi"] = INS[1]
			FU_STAT_["add"]["fj"] = INS[2]
			FU_STAT_["add"]["fk"] = INS[3]
			FU_STAT_["add"]["qj"] = REGS_STAT[INS[2]]
			FU_STAT_["add"]["qk"] = REGS_STAT[INS[3]]
			FU_STAT_["add"]["rj"] = not FU_STAT_["add"]["qj"]
			FU_STAT_["add"]["rk"] = not FU_STAT_["add"]["qk"]
			FU_STAT_["add"]["num"] = i
			REGS_STAT[INS[1]] = "add"
			flag_is = 1
	elif(INS[0] == "sub"):
		if(not FU_STAT["add"]["busy"] and not REGS_STAT[INS[1]]):
			FU_STAT_["add"]["busy"] = True
			FU_STAT_["add"]["op"] = "sub"
			FU_STAT_["add"]["fi"] = INS[1]
			FU_STAT_["add"]["fj"] = INS[2]
			FU_STAT_["add"]["fk"] = INS[3]
			FU_STAT_["add"]["qj"] = REGS_STAT[INS[2]]
			FU_STAT_["add"]["qk"] = REGS_STAT[INS[3]]
			FU_STAT_["add"]["rj"] = not FU_STAT_["add"]["qj"]
			FU_STAT_["add"]["rk"] = not FU_STAT_["add"]["qk"]
			FU_STAT_["add"]["num"] = i
			REGS_STAT[INS[1]] = "add"
			flag_is = 1
	# 如果可以发射指令，则更新指令状态表的当前指令行
	# 同时可以取下一条指令
	if flag_is:
		INS_STAT[i]["IS"] = c
		i += 1

	# RO阶段
	flag_ro = {fu:False for fu in FU}
	# 检查每条已发射指令
	for fu in FU:
		# 如果源操作数就绪，则可读取操作数，同时更新FU_STAT
		if FU_STAT[fu]["rj"] and FU_STAT[fu]["rk"]:
			FU_STAT_[fu]["rj"] = False
			FU_STAT_[fu]["rk"] = False
			FU_STAT_[fu]["qj"] = ""
			FU_STAT_[fu]["qk"] = ""
			flag_ro[fu] = True
			INS_STAT[FU_STAT_[fu]["num"]]["RO"] = c

	# EX
	for fu in FU:
		if flag_ex[fu]:
			INS_STAT[FU_STAT_[fu]["num"]]["EX"] = c

	# WR
	for fu in FU:
		# 对每条等待写回的指令
		if flag_wr[fu]:
			flag_wr_ = 1 # 功能单元fu所执行的指令是否可以写回
			# 判断是否有WAR冒险
			for fu_ in FU:
				if ((FU_STAT[fu_]["fj"] == FU_STAT[fu]["fi"] and FU_STAT[fu_]["rj"]) or
					(FU_STAT[fu_]["fk"] == FU_STAT[fu]["fi"] and FU_STAT[fu_]["rk"])):
					flag_wr_ = 0
					break
			# 如果没有WAR冒险，可以写回
			if flag_wr_:
				# 写回后修改对该指令有依赖的指令在功能单元状态表中对应的项
				for fu_ in FU:
					if FU_STAT[fu_]["qj"] == fu:
						FU_STAT_[fu_]["qj"] = ""
						FU_STAT_[fu_]["rj"] = True
					if FU_STAT[fu_]["qk"] == fu:
						FU_STAT_[fu_]["qk"] = ""
						FU_STAT_[fu_]["rk"] = True
				# 更新指令状态表
				INS_STAT[FU_STAT_[fu]["num"]]["WR"] = c
				# 释放寄存器状态表
				REGS_STAT[FU_STAT_[fu]["fi"]] = ""
				# 释放功能状态表项
				for k in FU_STAT_[fu].keys():
					FU_STAT_[fu][k] = ""
				flag_wr[fu] = False

	# 周期结束，更新状态
	# 更新功能状态表
	FU_STAT = FU_STAT_
	# 更新flag_wr
	# 包括本周期因WAR冒险不能写回的，加上EX阶段执行完的功能单元
	for fu in flag_wr.keys():
		flag_wr[fu] = flag_wr[fu] or flag_ex[fu]
	# 更新flag_ex为本周期成功读取源操作数的功能单元
	flag_ex = flag_ro
	# 随意输入进入下一周期
	input()

"""
ld f6 34 f1
ld f2 45 f3
mul f0 f2 f4
sub f8 f6 f2
div f10 f0 f6
add f6 f8 f2
"""