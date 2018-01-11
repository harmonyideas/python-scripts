
using System;
using System.Data;
using System.IO;
using MySql.Data.MySqlClient;
using System.Windows.Forms;

namespace WindowsFormsApplication1
{
    public interface IDBAdapter
    {
        IDatabaseAdapter CreateAdapter();
    }

    public class MySqlDatabaseAdapter : IDatabaseAdapter
    {
        private string _uid, _server, _pw, _db;

        public void InitilizeConnection(string _uid, string _server, string _pw, string _db)
        {
            try
            {
                System.Data.SqlClient.SqlConnectionStringBuilder cStringBuilder;
                this._uid = _uid;
                this._server = _server;
                this._pw = _pw;
                this._db = _db;

                // Check to make sure that our class was passed information
                // from the caller before we attempt to connect
                if (String.IsNullOrEmpty(_server))
                    throw new InvalidDataException("No Server Specified");
                if (String.IsNullOrEmpty(_uid))
                    throw new InvalidDataException("No Username Specified");
                if (String.IsNullOrEmpty(_pw))
                    throw new InvalidDataException("No Password Specified");
                if (String.IsNullOrEmpty(_db))
                    throw new InvalidDataException("No Database Specified");

                cStringBuilder = new System.Data.SqlClient.SqlConnectionStringBuilder();
                cStringBuilder.DataSource = _server;
                cStringBuilder.UserID = _uid;
                cStringBuilder.Password = _pw;
                cStringBuilder.InitialCatalog = _db;

                using (MySqlConnection _connection = new MySqlConnection(cStringBuilder.ToString()))
                {
                    if (_connection.State == ConnectionState.Closed)
                    {
                        _connection.Open();
                    }
                }
            }
            catch (MySql.Data.MySqlClient.MySqlException ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

    }

    public interface IDatabaseAdapter
    {
        void InitilizeConnection(string _uid, string _server, string _pw, string _db);
    }

    public class MySqlDataAdapter : IDBAdapter
    {
        public IDatabaseAdapter CreateAdapter()
        {
            return new MySqlDatabaseAdapter();
        }
    }

    public class DBClient
    {
        private IDatabaseAdapter _adapter;

        public DBClient(IDBAdapter adapter)
        {
            _adapter = adapter.CreateAdapter();
        }

        public IDatabaseAdapter Adapter
        {
            get { return _adapter; }
        }
    }
}
