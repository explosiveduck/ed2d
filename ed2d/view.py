from ed2d import idgen

class View(object):

    def __init__(self):

        self.sids = idgen.IdGenerator()
        self.programs = []
        self.uniforms = []
        self.uniformIds = []

        self.pids = idgen.IdGenerator()
        self.projections = []
        self.projNames = []
        self.progPerProj = []

    def new_projection(self, name, projection):
        pid = self.pids.gen_id()

        idgen.set_uid_list(self.projNames, pid, name)
        idgen.set_uid_list(self.projections, pid, projection)
        idgen.set_uid_list(self.progPerProj, pid, [])

    def set_projection(self, name, projection):
        pid = self.projNames.index(name)
        sids = self.progPerProj[pid]

        self.projections[pid] = projection

        for i in sids:
            program = self.programs[i-1]
            program.use()
            uniformId = self.uniformIds[i-1]
            program.set_uniform_matrix(uniformId, projection)

    def create_uniforms(self, name):
        pid = self.projNames.index(name)
        sids = self.progPerProj[pid]
        projection = self.projections[pid]

        for i in sids:
            program = self.programs[i-1]
            program.use()

            uniformId = program.new_uniform(name.encode('utf-8'))
            program.set_uniform_matrix(uniformId, projection)
            self.uniformIds[i-1] = uniformId


    def register_shader(self, projName, program):
        pid = self.projNames.index(projName)
        sid = self.sids.gen_id()
        print (sid)

        self.progPerProj[pid].append(sid)

        idgen.set_uid_list(self.programs, sid, program)
        idgen.set_uid_list(self.uniformIds, sid, [])

        self.create_uniforms(projName)
