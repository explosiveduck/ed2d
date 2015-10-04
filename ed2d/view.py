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

        idgen.set_uid_list(self.projections, pid, projection)
        idgen.set_uid_list(self.projNames, pid, name)
        idgen.set_uid_list(self.progPerProj, pid, [])

        self.create_uniforms(name)
        self.update_projection(name, projection)

    def create_uniforms(self, name):
        pid = self.projNames.index(name)
        sids = self.progPerProj[pid]

        for i in sids:
            program = self.programs[i]
            program.use()

            uniformId = program.new_uniform(name)
            self.uniformIds[i].append(uniformId)

    def set_uniforms(self, name):
        pid = self.projNames.index(name)
        sids = self.progPerProj[pid]
        projection = self.uniforms[pid]

        for i in sids:
            program = self.programs[i]
            program.use()
            uniformId = self.uniformIds[i]

            program.set_uniform_matrix(uniformId, projection)

    def update_projection(self, name, projection):
        pid = self.projNames.index(name)
        sids = self.progPerProj[pid]

        self.projections[pid] = projection

        self.set_uniforms()


    def register_shader(self, projection, program, uniform):
        pid = self.projNames.index(projection)
        sid = self.sids.gen_id()

        self.progPerProj[pid].append(sid)

        idgen.set_uid_list(self.programs, sid, program)
        idgen.set_uid_list(self.uniforms, sid, uniform)
        idgen.set_uid_list(self.uniformIds, sid, [])



