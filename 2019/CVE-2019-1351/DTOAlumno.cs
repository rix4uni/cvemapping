using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace FNT_BusinessEntities.Interface
{
    public class DTOAlumnoRespuesta
    {
        public DTOHeader DTOHeader { get; set; }

        public DTOAlumno DTOAlumno { get; set; }
        public List<DTOAlumno> ListaDTOAlumno { get; set; }

    }

    public class DTOAlumno
    {
        public string AlumnoCodigoLineaNegocio { get; set; }
        public string AlumnoCodigoAlumno { get; set; }
        public Int64 AlumnoCodigoPersona { get; set; }
        public string AlumnoCodigoUsuario { get; set; }
        public string AlumnoFlagCorreo { get; set; }
        public string AlumnoCodSede { get; set; }
        public string PersonaSexo { get; set; }
        public string PersonaApellidoPatern { get; set; }
        public string PersonaApellidoMatern { get; set; }
        public string PersonaNombres { get; set; }
        public string PersonaTipoDocumento { get; set; }
        public string PersonaDocumenIdentida { get; set; }
        public string UsuarioEmail { get; set; }
        public DateTime AlumnoFechaCreacion { get; set; }
        public string AlumnoUsuarioCreacion { get; set; }
        public Nullable<System.DateTime> AlumnoFechaModificacion { get; set; }
        public string AlumnoUsuarioModificacion { get; set; }

    }
}
