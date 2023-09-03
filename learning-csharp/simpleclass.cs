using System;
using System.Collections.Generic;

namespace MySimpleClass
{
    class Program
    {
        static void Main(string[] args)
        {
            List<Name> names = Name.AddNames();
            names.ForEach(i => Console.Write("{0}\r", i));
        }
    }
}

public class Name
{
    readonly string _strFirstName;
    public string FirstName { get { return _strFirstName; } }

    readonly string _strLastName;
    public string LastName { get { return _strLastName; } }

    public Name(string _strFirstName, string _strLastName)
    {
        this._strFirstName = _strFirstName;
        this._strLastName = _strLastName;
    }

    public static List<Name> AddNames()
    {
        return new List<Name>
            {
                new Name(_strFirstName: "Hello", _strLastName: "World")
            };
    }
    public override string ToString()
    {
        return string.Format("{0} {1}", FirstName, LastName);
    }
}
