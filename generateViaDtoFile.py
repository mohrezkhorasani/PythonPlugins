import re

def remove_dto_from_filename(file_path):
    try:
        file_name = os.path.basename(file_path)
        modified_file_name = file_name.replace("DTO.cs", "")
        return modified_file_name
    except:
        return None
# Initialize variables to store the generated code for each type
dto_content = f'''using FarabiCore.Application.DTO.Generals;
using FarabiCore.Application.Interface;
using FarabiCore.Application.Interface.UseCases;
using System.Collections.Generic;

namespace FarabiCore.Application.DTO.Front.App
{{
    '''
use_case_interface_content = f'''using FarabiCore.Application.DTO.Front.App;
using FarabiCore.Application.DTO.Generals;
using FarabiCore.Application.Interface.UseCases;

namespace FarabiCore.Application.Interface{{'''
use_case_content = f'''
using FarabiCore.Application.DTO.Front.App;
using FarabiCore.Application.DTO.Generals;
using FarabiCore.Application.Interface;
using System.Threading.Tasks;
using FarabiCore.Application.Interface;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using FarabiCore.Application.Commons;
using FarabiCore.Application.Interface.UseCases;
using FarabiCore.Application.Interface.Context;
using FarabiCore.Domain.Entities;
using System;
using FarabiCore.Application.UseCases;
using Microsoft.Extensions.Configuration;

namespace FarabiCore.Application.UseCase
{{
'''

# Function to create code
def generate_code(nameOfFile, regionName):
    if regionName == '.':
        return False  # Break the loop

    # Create [nameOfFile]DTO.cs content for the current regionName
    dto_code = f'''
    #region {regionName}
    public class {regionName}Request : BaseParentRequest, IUseCaseRequest<GenericResponse<{regionName}Response>>
    {{
        
    }}
    public class {regionName}Response : BaseParentResponce
    {{

    }}

    #endregion
    '''
    global dto_content
    dto_content += dto_code + '\n'

    # Create I[nameOfFile]UseCase.cs content for the current regionName
    use_case_interface_code = f'''public interface I{regionName}UseCase : IUseCaseRequestHandler<{regionName}Request, GenericResponse<{regionName}Response>>
    {{
    }}
    '''
    global use_case_interface_content
    use_case_interface_content += use_case_interface_code + '\n'

    # Create [nameOfFile]UseCase.cs content for the current regionName
    use_case_code = f'''
  #region {regionName}
  public class {regionName}UseCase : I{regionName}UseCase
  {{
      public IFarabiCMSCore2022DBContext db {{ get; }}
      public CommonMethods common {{ get; }}
      public {regionName}UseCase(IFarabiCMSCore2022DBContext db, IConfiguration configuration)
      {{
          this.db = db;
          this.common = new CommonMethods(configuration, db);
      }}

      public async Task handleAsync({regionName}Request message,
          IOutPutPort<GenericResponse<{regionName}Response>> outPutPort)
      {{
       
          outPutPort.Handle(new GenericResponse<{regionName}Response>(new {regionName}Response
          {{
              message = "OK!",
              status = 200
          }}));
      }}
  }}
  #endregion {regionName}
  '''
    global use_case_content
    use_case_content += use_case_code + '\n'

    return True

# Input value for nameOfFile

def extract_region_names_from_file(file_path):
    
    region_names = []

    try:
        with open(file_path, 'r') as file:
            csharp_code = file.read()

        pattern = r'#region (.*?)\n'
        region_names = re.findall(pattern, csharp_code)

    except FileNotFoundError:
        print(f"File not found at the specified path: {file_path}")

    return region_names


file_path = input("Enter the path to your C# file: ")
region_names = extract_region_names_from_file(file_path)
nameOfFile = remove_dto_from_filename(file_path)

if region_names:
    print("List of Region Names:")
    for regionName in region_names:
        generate_code(nameOfFile, regionName)
        

dto_content = dto_content+"\n}"
use_case_interface_content = use_case_interface_content+"\n}"
use_case_content = use_case_content+"\n}"
# Write the generated code to the files
with open(f'{nameOfFile}DTO.cs', 'a') as dto_file:
    dto_file.write(dto_content)

with open(f'I{nameOfFile}UseCase.cs', 'a') as interface_file:
    interface_file.write(use_case_interface_content)

with open(f'{nameOfFile}UseCase.cs', 'a') as use_case_file:
    use_case_file.write(use_case_content)
    
print("Code generation complete!")