import pinocchio as pin
from pinocchio import casadi as cpin
import casadi
import numpy as np
import os

class Arm_IK:
    # def __init__(self):
    #     # 初始化机器人模型、优化器等（这里简化）
    #     pass

    # def ik_fun(self, target_pose: np.ndarray, gripper: float = 0.0):
    #     """
    #     逆运动学求解函数示例
    #     :param target_pose: 4x4 numpy数组，目标末端位姿变换矩阵
    #     :param gripper: 夹爪开合度（示例参数）
    #     :return: sol_q: 关节角度数组（示例7自由度）
    #              tau_ff: 关节力矩（示例空数组）
    #              is_collision: 是否碰撞（示例False）
    #     """
    #     # 这里用简单模拟数据代替真实逆运动学计算
    #     sol_q = np.array([0.1, 0.2, -0.1, 0.5, -0.3, 0.4, gripper])
    #     tau_ff = np.zeros_like(sol_q)
    #     is_collision = False
    #     return sol_q, tau_ff, is_collision
    
    def __init__(self, urdf_path: str, base_joint_name: str = 'base_link', ee_frame_name: str = 'ee'):
        # 加载机器人模型
        self.robot = pin.RobotWrapper.BuildFromURDF(urdf_path, package_dirs=os.path.dirname(urdf_path))
        self.model = self.robot.model
        self.data = self.robot.data

        # 末端执行器帧ID
        self.ee_frame_id = self.model.getFrameId(ee_frame_name)

        # Casadi模型和数据
        self.cmodel = cpin.Model(self.model)
        self.cdata = self.cmodel.createData()

        # 定义Casadi符号变量
        self.cq = casadi.SX.sym('q', self.model.nq)
        self.cTf = casadi.SX.sym('Tf', 4, 4)

        # 计算正运动学
        cpin.framesForwardKinematics(self.cmodel, self.cdata, self.cq)

        # 误差函数（末端位姿误差）
        error_vec = cpin.log6(self.cdata.oMf[self.ee_frame_id].inverse() * cpin.SE3(self.cTf)).vector
        self.error_func = casadi.Function('error', [self.cq, self.cTf], [error_vec])

        # 优化器
        self.opti = casadi.Opti()
        self.var_q = self.opti.variable(self.model.nq)
        self.param_tf = self.opti.parameter(4, 4)

        # 目标误差平方和
        error = self.error_func(self.var_q, self.param_tf)
        pos_error = error[:3]
        ori_error = error[3:]
        w_pos = 1.0
        w_ori = 0.1
        cost = casadi.sumsqr(w_pos * pos_error) + casadi.sumsqr(w_ori * ori_error)

        # 关节限制约束
        self.opti.subject_to(self.opti.bounded(self.model.lowerPositionLimit, self.var_q, self.model.upperPositionLimit))

        # 最小化目标函数
        self.opti.minimize(cost)

        # IPOPT求解器配置
        opts = {'ipopt.print_level': 0, 'print_time': False, 'ipopt.max_iter': 100, 'ipopt.tol': 1e-4}
        self.opti.solver('ipopt', opts)

        # 初始解
        self.initial_guess = np.zeros(self.model.nq)

    def ik_fun(self, target_pose: np.ndarray, initial_guess: np.ndarray = None):
        """
        求解逆运动学
        :param target_pose: 4x4目标末端位姿矩阵
        :param initial_guess: 初始关节角度猜测
        :return: 关节角度解（numpy数组），是否成功
        """
        if initial_guess is None:
            initial_guess = self.initial_guess

        self.opti.set_value(self.param_tf, target_pose)
        self.opti.set_initial(self.var_q, initial_guess)

        try:
            sol = self.opti.solve()
            q_sol = sol.value(self.var_q)
            self.initial_guess = q_sol  # 更新初始猜测
            return q_sol, True
        except RuntimeError as e:
            print(f"IK求解失败: {e}")
            return None, False


'''
import pinocchio as pin
from pinocchio import casadi as cpin
import casadi
import numpy as np
import os

class ArmIK:
    def __init__(self, urdf_path: str, base_joint_name: str = 'base_link', ee_frame_name: str = 'ee'):
        # 加载机器人模型
        self.robot = pin.RobotWrapper.BuildFromURDF(urdf_path, package_dirs=os.path.dirname(urdf_path))
        self.model = self.robot.model
        self.data = self.robot.data

        # 末端执行器帧ID
        self.ee_frame_id = self.model.getFrameId(ee_frame_name)

        # Casadi模型和数据
        self.cmodel = cpin.Model(self.model)
        self.cdata = self.cmodel.createData()

        # 定义Casadi符号变量
        self.cq = casadi.SX.sym('q', self.model.nq)
        self.cTf = casadi.SX.sym('Tf', 4, 4)

        # 计算正运动学
        cpin.framesForwardKinematics(self.cmodel, self.cdata, self.cq)

        # 误差函数（末端位姿误差）
        error_vec = cpin.log6(self.cdata.oMf[self.ee_frame_id].inverse() * cpin.SE3(self.cTf)).vector
        self.error_func = casadi.Function('error', [self.cq, self.cTf], [error_vec])

        # 优化器
        self.opti = casadi.Opti()
        self.var_q = self.opti.variable(self.model.nq)
        self.param_tf = self.opti.parameter(4, 4)

        # 目标误差平方和
        error = self.error_func(self.var_q, self.param_tf)
        pos_error = error[:3]
        ori_error = error[3:]
        w_pos = 1.0
        w_ori = 0.1
        cost = casadi.sumsqr(w_pos * pos_error) + casadi.sumsqr(w_ori * ori_error)

        # 关节限制约束
        self.opti.subject_to(self.opti.bounded(self.model.lowerPositionLimit, self.var_q, self.model.upperPositionLimit))

        # 最小化目标函数
        self.opti.minimize(cost)

        # IPOPT求解器配置
        opts = {'ipopt.print_level': 0, 'print_time': False, 'ipopt.max_iter': 100, 'ipopt.tol': 1e-4}
        self.opti.solver('ipopt', opts)

        # 初始解
        self.initial_guess = np.zeros(self.model.nq)

    def solve_ik(self, target_pose: np.ndarray, initial_guess: np.ndarray = None):
        """
        求解逆运动学
        :param target_pose: 4x4目标末端位姿矩阵
        :param initial_guess: 初始关节角度猜测
        :return: 关节角度解（numpy数组），是否成功
        """
        if initial_guess is None:
            initial_guess = self.initial_guess

        self.opti.set_value(self.param_tf, target_pose)
        self.opti.set_initial(self.var_q, initial_guess)

        try:
            sol = self.opti.solve()
            q_sol = sol.value(self.var_q)
            self.initial_guess = q_sol  # 更新初始猜测
            return q_sol, True
        except RuntimeError as e:
            print(f"IK求解失败: {e}")
            return None, False

'''